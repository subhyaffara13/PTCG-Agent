
def _score_single_option(opt, registry, board_pokemon_names, sel_type, select, observation):
    from ._resolve_opt_card import _resolve_card_id
    current = observation.get("current")
    my_idx = current.get("yourIndex", 0) if current else 0
    card_id = _resolve_card_id(opt, current, my_idx)
    card_name = opt.get("name", "")
    card = None
    if card_id is not None:
        card = registry.get_full_skill(card_id)
    if card is None and card_name:
        card = registry.get_full_skill(card_name)
    score = 0.0
    if not card:
        return (0, score)
    score = getattr(card, "utility_score", 0.0)
    card_id_int = getattr(card, "card_id", None)
    if card_id_int is not None:
        if hasattr(registry, "learned_dos") and int(card_id_int) in registry.learned_dos:
            score += 12.0
        if hasattr(registry, "learned_donts") and int(card_id_int) in registry.learned_donts:
            score -= 12.0
    predecessor = registry.get_evolution_predecessor(getattr(card, "card_name", ""))
    if predecessor and predecessor.lower() in board_pokemon_names:
        score += 15.0
    score = _score_energy_attach(score, opt, card, registry, sel_type, select, current, my_idx)
    turn = current.get("turn", 1) if current else 1
    if turn <= 5:
        support_names = {"bidoof", "bibarel", "snom", "frosmoth", "remoraid", "octillery", "dunsparce", "jirachi", "manaphy", "mew"}
        card_name_lower = getattr(card, "card_name", "").lower()
        if any(s in card_name_lower for s in support_names):
            score += 15.0
    if sel_type == 3:
        score += getattr(card, "ev_score", 0.0) + (getattr(card, "damage_output", 0) * 0.01)
    return (0, score)

