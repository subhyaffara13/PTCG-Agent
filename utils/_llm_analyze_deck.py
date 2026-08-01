
def _llm_analyze_deck(card_names, learned_donts, save_donts_fn):
    import os, json, requests
    from dotenv import load_dotenv
    from collections import Counter
    load_dotenv()
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not gemini_key or not card_names: return False
    counts = Counter(card_names)
    deck_str = "\n".join(f"{name} (x{count})" for name, count in counts.items())
    prompt = f"Identify toxic ratios, dead-draw packages, element-type mismatches:\n```\n{deck_str}\n```\nOutput JSON with 'deck_donts' list."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
        if res.status_code == 200:
            data = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(data)
            donts = parsed.get("deck_donts", [])
            changed = False
            for rule in donts:
                if rule not in learned_donts["deck_donts"]: learned_donts["deck_donts"].append(rule); changed = True
            if changed: save_donts_fn(); return True
    except Exception: pass
    return False

