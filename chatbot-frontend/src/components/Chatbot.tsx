import React, { useState, useRef, useEffect } from 'react'
import { HiOutlinePaperAirplane, HiTrash, HiOutlineClock, HiTranslate } from 'react-icons/hi'

type Result = {
  Name: string
  URL: string
  Summary: string
  Category?: string
  Score?: number
}

type Message = {
  id: string
  sender: 'user' | 'bot'
  text?: string
  results?: Result[]
}

export default function Chatbot() {
  const [message, setMessage] = useState('')
  const MAX_CHARS = 1000
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [error, setError] = useState<string | null>(null)
  const [history, setHistory] = useState<string[]>(() => {
    try {
      const raw = localStorage.getItem('npc_history')
      return raw ? JSON.parse(raw) : []
    } catch {
      return []
    }
  })
  const inputRef = useRef<HTMLTextAreaElement | null>(null)
  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  function addUserMessage(text: string) {
    const msg: Message = { id: String(Date.now()), sender: 'user', text }
    setMessages((m) => [...m, msg])
  }

  function addBotMessage(results: Result[] | null, text?: string) {
    const msg: Message = { id: String(Date.now()), sender: 'bot', results: results || [], text }
    setMessages((m) => [...m, msg])
  }

  async function sendMessage() {
    if (!message.trim()) return
    if (message.length > MAX_CHARS) {
      setError(`Message too long (max ${MAX_CHARS} characters)`)
      return
    }
    setError(null)
  addUserMessage(message.trim())
    setLoading(true)

    try {
      // Try relative path first (works when Vite proxy is enabled). Fallback to direct backend URL.
      const urlsToTry = ['/api/chat', 'http://127.0.0.1:8000/api/chat']
      let resp: Response | null = null
      let lastErr: any = null

      for (const url of urlsToTry) {
        try {
          resp = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message.trim(), top_k: 5 }),
          })
          // If fetched (even 4xx/5xx), stop trying other URLs and handle below
          break
        } catch (err) {
          lastErr = err
        }
      }

      if (!resp) throw lastErr || new Error('Failed to reach backend')

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({ detail: resp.statusText }))
        throw new Error(err.detail || 'Server error')
      }

      const data = await resp.json()

      // Expecting { query_info: {...}, results: [...] }
      const results: Result[] = Array.isArray(data.results) ? data.results : []
      const translated = data?.query_info?.translated ?? data?.query_info?.original ?? ''
      addBotMessage(results, translated)
      // Save to local history (most recent first), dedupe and keep max 20
      try {
        const q = message.trim()
        if (q) {
          setHistory((h) => {
            const deduped = [q, ...h.filter((x) => x !== q)].slice(0, 20)
            localStorage.setItem('npc_history', JSON.stringify(deduped))
            return deduped
          })
        }
      } catch {}
    } catch (e: any) {
      setError(e.message || 'Unknown error')
      addBotMessage([], 'Sorry, I could not fetch results.')
    } finally {
      setLoading(false)
      // Focus and select the input so the user can immediately replace the query and press Send
      setTimeout(() => {
        inputRef.current?.focus()
        try { inputRef.current?.select() } catch (e) {}
      }, 50)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  function clearConversation() {
    // Clear conversation history but keep the input focused so a new query can be typed immediately
    setMessages([])
    setError(null)
    setTimeout(() => inputRef.current?.focus(), 50)
  }

  function selectHistory(q: string) {
    setMessage(q)
    setTimeout(() => {
      inputRef.current?.focus()
      try { inputRef.current?.select() } catch {}
    }, 50)
  }

  function clearHistory() {
    setHistory([])
    try { localStorage.removeItem('npc_history') } catch {}
  }

  return (
    <div className="chatbot">
      <div className="chat-top">
        <div style={{display:'flex',alignItems:'center',gap:10}}>
          <div className="title">Ask about nonprofit resources</div>
          <div style={{display:'flex',alignItems:'center',gap:6,color:'var(--muted)'}}><HiTranslate /> Spanish & English</div>
        </div>
        <div className="subtitle">Fast semantic matching · Multilingual</div>
      </div>
      <div className="chat-controls">
        <div className="history-bar">
          <label htmlFor="recent">Recent:</label>
          <select id="recent" onChange={(e) => selectHistory(e.target.value)} value="">
            <option value="">— pick recent query —</option>
            {history.map((h, i) => (
              <option key={i} value={h}>{h}</option>
            ))}
          </select>
          <button onClick={clearHistory} className="muted small"><HiOutlineClock style={{verticalAlign:'middle'}}/> Clear history</button>
        </div>
        <textarea
          ref={inputRef}
          value={message}
          onChange={(e) => {
            const val = e.target.value
            if (val.length <= MAX_CHARS) setMessage(val)
            else setMessage(val.slice(0, MAX_CHARS))
          }}
          onKeyDown={handleKeyDown}
          onPaste={(e) => {
            const paste = (e.clipboardData || (window as any).clipboardData).getData('text') || ''
            const allowed = MAX_CHARS - message.length
            if (paste.length > allowed) {
              e.preventDefault()
              setMessage((m) => (m + paste.slice(0, allowed)))
            }
          }}
          placeholder="Ask about nonprofit resources (Enter to send, Shift+Enter for new line)"
          rows={3}
        />
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div className="char-counter">{message.length}/{MAX_CHARS}</div>
          <div style={{display:'flex',gap:8}}>
            <div style={{color:'var(--muted)',fontSize:12,marginRight:6}}>{messages.length} messages</div>
          </div>
        </div>
        <div className="actions">
          <button onClick={sendMessage} disabled={loading}>
            {loading ? 'Searching...' : <><HiOutlinePaperAirplane style={{verticalAlign:'middle',marginRight:8}}/>Send</>}
          </button>
          <button onClick={clearConversation} className="muted">
            <HiTrash style={{verticalAlign:'middle',marginRight:6}}/> Clear
          </button>
        </div>
      </div>

      <div className="chat-results">
        {messages.length === 0 && !loading && <div className="empty">No conversation yet. Ask something to start.</div>}

        {messages.map((m) => (
          <div key={m.id} className={`message ${m.sender}`}>
            {m.sender === 'user' && <div className="bubble user">{m.text}</div>}
            {m.sender === 'bot' && (
              <div className="bubble bot">
                {m.text && <div className="bot-text">Translated: {m.text}</div>}
                {m.results && m.results.length > 0 ? (
                  <div className="results">
                    {m.results.map((r, i) => (
                      <article key={i} className="result-card">
                        <h3><a href={r.URL} target="_blank" rel="noreferrer">{r.Name}</a></h3>
                        <div className="meta">{r.Category} — {r.Score?.toFixed(4)}</div>
                        <p>{r.Summary}</p>
                      </article>
                    ))}
                  </div>
                ) : (
                  <div className="no-results">No results returned.</div>
                )}
              </div>
            )}
          </div>
        ))}

        <div ref={bottomRef} />
      </div>
    </div>
  )
}
