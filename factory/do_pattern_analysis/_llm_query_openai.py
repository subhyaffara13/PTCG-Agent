import json, logging, os, requests
logger = logging.getLogger("DoPatternAnalysis")

def _query_openai(prompt, extractor):
    openai_key = os.environ.get("OPENAI_API_KEY")
    openai_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1") + "/chat/completions"
    if not openai_key:
        return False, []
    logger.info("DoPatternAnalysis: Querying OpenAI...")
    payload = {
        "model": "gpt-4o-mini",
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "You are a Pokemon TCG AI analyst. Return JSON with key 'deck_dos'."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        headers = {"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"}
        res = requests.post(openai_url, json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            content_str = res.json()["choices"][0]["message"]["content"]
            parsed = json.loads(content_str)
            new_dos = parsed.get("deck_dos", [])
            for item in new_dos:
                existing = next((x for x in extractor.learned_dos["deck_dos"] if int(x.get("card_id", 0)) == int(item["card_id"])), None)
                if existing:
                    existing["avg_count"] = max(existing.get("avg_count", 0), item["avg_count"])
                    existing["reason"] = item["reason"]
                else:
                    extractor.learned_dos["deck_dos"].append(item)
            logger.info(f"Merged {len(new_dos)} OpenAI card synergies.")
            return True, new_dos
    except Exception as e:
        logger.warning(f"OpenAI extraction failed: {e}.")
    return False, []
