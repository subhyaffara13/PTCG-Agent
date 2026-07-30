def _get_player_idx(steps, info, team_names, name_or_id) -> int:
    if str(name_or_id).isdigit():
        if len(steps) > 1:
            for idx, p_state in enumerate(steps[1]):
                obs = p_state.get("observation") or {} if p_state else {}
                players = (obs.get("current") or {}).get("players", [])
                if idx < len(players) and str(players[idx].get("teamId")) == str(name_or_id):
                    return idx
    else:
        for idx, name in enumerate(team_names):
            if name_or_id.lower() in name.lower():
                return idx
    return -1

def _count_deck_types(deck) -> tuple:
    from cb_agents.card_registry import CardRegistry
    from cb_agents.card_types import CardType
    reg = CardRegistry()
    p_c, t_c, e_c = 0, 0, 0
    for cid in deck:
        c = reg.get(cid)
        if c:
            if c.card_type == CardType.POKEMON: p_c += 1
            elif c.card_type == CardType.TRAINER: t_c += 1
            elif c.card_type == CardType.ENERGY: e_c += 1
        else:
            if cid <= 20: e_c += 1
            else: t_c += 1
    return p_c, t_c, e_c

