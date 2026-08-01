
def _query_gemini(prompt, extractor):
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not gemini_key:
        return False, []
    logger.info("DoPatternAnalysis: Querying Google Gemini...")
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "deck_dos": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "card_id": {"type": "INTEGER"},
                                "avg_count": {"type": "NUMBER"},
                                "reason": {"type": "STRING"}
                            },
                            "required": ["card_id", "avg_count", "reason"]
                        }
                    }
                },
                "required": ["deck_dos"]
            }
        }
    }
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={gemini_key}"
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
        if res.status_code == 200:
            data = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(data)
            new_dos = parsed.get("deck_dos", [])
            for item in new_dos:
                existing = next((x for x in extractor.learned_dos["deck_dos"] if int(x.get("card_id", 0)) == int(item["card_id"])), None)
                if existing:
                    existing["avg_count"] = max(existing.get("avg_count", 0), item["avg_count"])
                    existing["reason"] = item["reason"]
                else:
                    extractor.learned_dos["deck_dos"].append(item)
            logger.info(f"Merged {len(new_dos)} Gemini card synergies.")
            return True, new_dos
    except Exception as e:
        logger.warning(f"Gemini extraction failed: {e}.")
    return False, []

