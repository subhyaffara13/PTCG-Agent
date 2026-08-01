
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

