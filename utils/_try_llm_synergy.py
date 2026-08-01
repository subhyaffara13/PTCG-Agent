
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

