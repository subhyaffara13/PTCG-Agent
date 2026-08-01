
def _baseline_fallback(card_counter, total_wins, extractor):
    deck_dos = [{"card_id": int(cid), "avg_count": round(cnt / total_wins, 2),
        "reason": "High usage in winning matches."}
        for cid, cnt in card_counter.items() if (cnt / total_wins) >= 1.5]
    for new_do in deck_dos:
        existing = next((item for item in extractor.learned_dos["deck_dos"]
                        if item["card_id"] == new_do["card_id"]), None)
        if existing: existing["avg_count"] = max(existing.get("avg_count", 0), new_do["avg_count"])
        else: extractor.learned_dos["deck_dos"].append(new_do)

