from langdetect import detect
from googletrans import Translator
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import spacy
import torch

# === Load Models and Resources ===
print("Loading models and data...")

# NLP
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")
translator = Translator()

# SBERT Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load DataFrame
df = pd.read_csv("all_nonprofits.csv")
df["Summary"] = df["Summary"].fillna("")

# Load SBERT embeddings
loaded_embeddings = np.load("summary_embeddings.npy")
summary_embeddings = torch.tensor(loaded_embeddings)

# Intent keywords
INTENT_KEYWORDS = {
    "food": ["food", "hunger", "meal", "pantry", "eat"],
    "housing": ["housing", "rent", "shelter", "home", "eviction"],
    "job": ["job", "work", "employment", "hire", "career"]
}


# === NLP + Search Pipeline ===

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate_to_english(text, lang):
    if lang != "en":
        try:
            return translator.translate(text, src=lang, dest="en").text
        except:
            return text
    return text

def extract_intent(text):
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in text.lower() for kw in keywords):
            return intent
    return "unknown"

def extract_entities(text, lang):
    doc = nlp_en(text) if lang == "en" else nlp_es(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def process_message(text):
    lang = detect_language(text)
    translated = translate_to_english(text, lang)
    intent = extract_intent(translated)
    entities = extract_entities(translated, lang)
    return {
        "original": text,
        "language": lang,
        "translated": translated,
        "intent": intent,
        "entities": entities
    }

def get_top_matches(user_input, top_k=5):
    processed = process_message(user_input)
    query = processed["translated"]
    query_embedding = model.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, summary_embeddings)[0]
    top_results = cos_scores.topk(k=top_k)

    matches = []
    for score, idx in zip(top_results[0], top_results[1]):
        idx = int(idx)
        matches.append({
            "Name": df.iloc[idx]["Name"],
            "URL": df.iloc[idx]["URL"],
            "Summary": df.iloc[idx]["Summary"],
            "Category": df.iloc[idx]["Category"],
            "Score": float(score)
        })

    return {
        "query_info": processed,
        "results": matches
    }


# === Terminal Interface ===
if __name__ == "__main__":
    print("Multilingual Nonprofit Finder (type 'exit' to quit)")
    while True:
        user_input = input("\nYour question: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        result = get_top_matches(user_input)

        print("\nDetected language:", result['query_info']['language'])
        print("Translated query:", result['query_info']['translated'])
        print("Intent:", result['query_info']['intent'])
        print("Entities:", result['query_info']['entities'])
        print("\nTop nonprofit matches:")

        for r in result["results"]:
            print(f"\nName: {r['Name']} (Score: {r['Score']:.4f})")
            print(f"URL: {r['URL']}")
            print(f"Summary: {r['Summary'][:200]}...")
