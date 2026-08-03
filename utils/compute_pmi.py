import math
from factory.deck_synergy_graph import SynergyGraph


def compute_pmi(card_a: int, card_b: int, graph: SynergyGraph) -> float:
    if card_a > card_b:
        card_a, card_b = card_b, card_a
        
    co_occur = graph.co_occurrence.get((card_a, card_b), 0)
    if co_occur == 0:
        return 0.0
        
    p_a = graph.card_counts.get(card_a, 0) / graph.total_decks
    p_b = graph.card_counts.get(card_b, 0) / graph.total_decks
    p_ab = co_occur / graph.total_decks
    
    if p_a == 0 or p_b == 0:
        return 0.0
        
    return math.log2(p_ab / (p_a * p_b))

