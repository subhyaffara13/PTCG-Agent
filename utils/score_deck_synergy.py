
def score_deck_synergy(deck: list, graph: SynergyGraph) -> float:
    total_pmi = 0.0
    card_ids = []
    for c in deck:
        if isinstance(c, dict) and "card_id" in c:
            try:
                card_ids.append(int(c["card_id"]))
            except Exception:
                pass
        elif isinstance(c, (int, str)) and str(c).isdigit():
            card_ids.append(int(c))
    n = len(card_ids)
    
    for i in range(n):
        for j in range(i + 1, n):
            total_pmi += graph.get_pmi(card_ids[i], card_ids[j])
            
    return total_pmi

