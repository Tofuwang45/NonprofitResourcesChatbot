from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Any
import traceback
import importlib
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
import time

# Globals to hold the imported module/function and any import-time error
main_module: Optional[Any] = None
get_top_matches: Optional[Any] = None
_import_error: Optional[BaseException] = None

# Configurable timeouts (seconds)
# Increased defaults to accommodate model downloads and slower machines
IMPORT_TIMEOUT = 120
REQUEST_TIMEOUT = 60


def try_import_main(timeout: int = IMPORT_TIMEOUT) -> bool:
    """Attempt to import `main.get_top_matches` with a timeout.

    The import runs in a background thread and we wait up to `timeout` seconds.
    If it completes successfully we store `get_top_matches` in the module global.
    If it times out or raises, we store the error in `_import_error` and return False.
    """
    global get_top_matches, _import_error
    if get_top_matches is not None:
        return True

    def _import():
        # Import the whole main module so we can inspect df/embeddings sizes
        m = importlib.import_module("main")
        fn = getattr(m, "get_top_matches")
        return m, fn

    with ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(_import)
        try:
            m, fn = future.result(timeout=timeout)
            global main_module
            main_module = m
            get_top_matches = fn
            _import_error = None
            return True
        except FutureTimeout:
            _import_error = TimeoutError(f"Import timed out after {timeout} seconds")
            return False
        except Exception as e:
            _import_error = e
            return False


app = FastAPI(title="Nonprofit Resources Chatbot API")

# Allow cross-origin requests (useful for local frontend development). Adjust in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    top_k: Optional[int] = 5


MAX_MESSAGE_CHARS = 2000
MAX_TOP_K = 20
MIN_TOP_K = 1


@app.on_event("startup")
def on_startup():
    # Try a timed import on startup so the API can start even if model loading is slow.
    started = time.time()
    ok = try_import_main()
    elapsed = time.time() - started
    if not ok:
        print(f"Warning: backend import did not complete within {IMPORT_TIMEOUT}s (elapsed={elapsed:.1f}s): {_import_error}")
    else:
        print(f"Backend loaded in {elapsed:.1f}s")


@app.post("/api/chat")
def chat(req: ChatRequest):
    """Accepts a user message and returns semantic-search results produced by `get_top_matches` in `main.py`.

    This endpoint enforces a per-request execution timeout so slow model calls return a 504 instead of hanging.
    """
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    # Validate input sizes
    if len(req.message) > MAX_MESSAGE_CHARS:
        raise HTTPException(status_code=400, detail=f"Message too long (max {MAX_MESSAGE_CHARS} chars)")

    # Clamp top_k to a safe range
    if req.top_k is None:
        req.top_k = 5
    else:
        if req.top_k < MIN_TOP_K or req.top_k > MAX_TOP_K:
            raise HTTPException(status_code=400, detail=f"top_k must be between {MIN_TOP_K} and {MAX_TOP_K}")

    # Further clamp top_k to the number of available items if we can detect it
    try:
        n_items = None
        if main_module is not None:
            # main may expose df or summary_embeddings
            if hasattr(main_module, 'df') and getattr(main_module, 'df') is not None:
                n_items = len(getattr(main_module, 'df'))
            elif hasattr(main_module, 'summary_embeddings') and getattr(main_module, 'summary_embeddings') is not None:
                n_items = getattr(main_module, 'summary_embeddings').shape[0]
        if n_items is not None and req.top_k > n_items:
            req.top_k = int(n_items)
    except Exception:
        # Ignore detection errors and keep the earlier clamped value
        pass

    # Coerce message to string
    try:
        req.message = str(req.message)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid message type")

    # Ensure backend is loaded; try again with a short timeout if needed
    if get_top_matches is None:
        imported = try_import_main(timeout=IMPORT_TIMEOUT)
        if not imported:
            # Import failed or timed out
            raise HTTPException(status_code=503, detail=f"Search backend not available: {_import_error}")

    # Run the search in a thread and enforce REQUEST_TIMEOUT
    with ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(get_top_matches, req.message, req.top_k)
        try:
            result = future.result(timeout=REQUEST_TIMEOUT)
            return result
        except FutureTimeout:
            # Optionally cancel the future (thread will continue running in background)
            raise HTTPException(status_code=504, detail=f"Search timed out after {REQUEST_TIMEOUT} seconds")
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "backend_loaded": get_top_matches is not None,
        "import_error": str(_import_error) if _import_error else None,
    }


if __name__ == "__main__":
    # Run the API with uvicorn when executed directly: `python api.py`
    import uvicorn

    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")
