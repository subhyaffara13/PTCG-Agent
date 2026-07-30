def _try_llm_synergy(player_name_or_id, card_counter, extractor):
    from cb_agents.card_registry import CardRegistry
    from ._llm_query_gemini import _query_gemini
    from ._llm_query_openai import _query_openai
    from ._llm_query_openrouter import _query_openrouter
    reg = CardRegistry()
    frequent_card_names = []
    for cid, cnt in card_counter.most_common(15):
        c = reg.get(cid)
        if c: frequent_card_names.append(f"{c.card_name} (card_id: {cid}, count_in_wins: {cnt})")
    if not frequent_card_names: return False, []
    prompt = (f"... You are an expert Pokemon TCG Deck Architect... [{player_name_or_id}]... "
              f"{chr(10).join(frequent_card_names)} ...")
    success, dos = _query_gemini(prompt, extractor)
    if not success: success, dos = _query_openai(prompt, extractor)
    if not success: success, dos = _query_openrouter(prompt, extractor)
    return success, dos

def _baseline_fallback(card_counter, total_wins, extractor):
    deck_dos = [{"card_id": int(cid), "avg_count": round(cnt / total_wins, 2),
        "reason": "High usage in winning matches."}
        for cid, cnt in card_counter.items() if (cnt / total_wins) >= 1.5]
    for new_do in deck_dos:
        existing = next((item for item in extractor.learned_dos["deck_dos"]
                        if item["card_id"] == new_do["card_id"]), None)
        if existing: existing["avg_count"] = max(existing.get("avg_count", 0), new_do["avg_count"])
        else: extractor.learned_dos["deck_dos"].append(new_do)
