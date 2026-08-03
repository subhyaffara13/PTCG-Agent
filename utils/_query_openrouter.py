import json
import os

def _query_openrouter(prompt, extractor):
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    if not openrouter_key:
        return False, []
    logger.info("DoPatternAnalysis: Querying OpenRouter...")
    payload = {
        "model": "google/gemini-2.5-flash:free",
        "messages": [
            {"role": "system", "content": "You are a Pokemon TCG AI analyst. Return JSON with key 'deck_dos'."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        headers = {"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"}
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            content_str = res.json()["choices"][0]["message"]["content"]
            if "```json" in content_str:
                content_str = content_str.split("```json")[1].split("```")[0].strip()
            elif "```" in content_str:
                content_str = content_str.split("```")[1].split("```")[0].strip()
            parsed = json.loads(content_str)
            new_dos = parsed.get("deck_dos", [])
            for item in new_dos:
                existing = next((x for x in extractor.learned_dos["deck_dos"] if int(x.get("card_id", 0)) == int(item["card_id"])), None)
                if existing:
                    existing["avg_count"] = max(existing.get("avg_count", 0), item["avg_count"])
                    existing["reason"] = item["reason"]
                else:
                    extractor.learned_dos["deck_dos"].append(item)
            logger.info(f"Merged {len(new_dos)} OpenRouter card synergies.")
            return True, new_dos
    except Exception as e:
        logger.warning(f"OpenRouter extraction failed: {e}.")
    return False, []

