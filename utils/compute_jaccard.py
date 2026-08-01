
def compute_jaccard(card_a: int, card_b: int, graph: SynergyGraph) -> float:
    if card_a > card_b:
        card_a, card_b = card_b, card_a
        
    co_occur = graph.co_occurrence.get((card_a, card_b), 0)
    if co_occur == 0:
        return 0.0
        
    count_a = graph.card_counts.get(card_a, 0)
    count_b = graph.card_counts.get(card_b, 0)
    
    union = count_a + count_b - co_occur
    if union == 0:
        return 0.0
        
    return co_occur / union

