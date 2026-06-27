import json
import math
import os
from collections import defaultdict
from typing import List, Set, Dict, Any, Tuple

class SynergyGraph:
    def __init__(self):
        self.co_occurrence = defaultdict(int)
        self.card_counts = defaultdict(int)
        self.total_decks = 0
        self.pmi_cache = {}
        
    def build_from_corpus(self, corpus: List[List[int]]):
        self.total_decks = len(corpus)
        for deck in corpus:
            unique_cards = set(deck)
            for card in unique_cards:
                self.card_counts[card] += 1
            
            cards_list = list(unique_cards)
            for i in range(len(cards_list)):
                for j in range(i + 1, len(cards_list)):
                    c1, c2 = cards_list[i], cards_list[j]
                    if c1 > c2:
                        c1, c2 = c2, c1
                    self.co_occurrence[(c1, c2)] += 1
        self.pmi_cache.clear()

    def get_pmi(self, card_a: int, card_b: int) -> float:
        if card_a > card_b:
            card_a, card_b = card_b, card_a
        
        pair = (card_a, card_b)
        if pair in self.pmi_cache:
            return self.pmi_cache[pair]
            
        pmi = compute_pmi(card_a, card_b, self)
        self.pmi_cache[pair] = pmi
        return pmi

    def extract_core_engines(self, threshold: float = 1.0) -> List[Set[int]]:
        """Identifies clusters of highly co-occurring cards."""
        # Simple connected components based on PMI threshold
        nodes = list(self.card_counts.keys())
        adj = {n: [] for n in nodes}
        for (c1, c2), count in self.co_occurrence.items():
            if self.get_pmi(c1, c2) >= threshold:
                adj[c1].append(c2)
                adj[c2].append(c1)
        
        visited = set()
        engines = []
        for n in nodes:
            if n not in visited:
                comp = set()
                q = [n]
                visited.add(n)
                while q:
                    curr = q.pop(0)
                    comp.add(curr)
                    for neighbor in adj[curr]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            q.append(neighbor)
                if len(comp) > 1: # Only care about engines with >1 card
                    engines.append(comp)
        return engines


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


def score_deck_synergy(deck: list, graph: SynergyGraph) -> float:
    # deck is a list of card dicts, or just card IDs?
    # Based on deck_synergy.py, deck is a list of dicts: c["card_id"]
    # We want sum of pairwise PMI scores for all card pairs in the 60-card deck
    # Wait, sum of pairwise PMI for unique pairs? Or all 60*59/2 pairs?
    # Usually it's unique pairs or weighted by counts. Let's do unique pairs for now, or just all pairs.
    # Actually, if we do all 60*59/2 pairs, it weights by frequency in the deck.
    total_pmi = 0.0
    card_ids = [str(c["card_id"]) for c in deck if "card_id" in c]
    n = len(card_ids)
    
    # Let's do unique pairs to avoid overweighting 4-ofs, 
    # but maybe all pairs is better. Let's do all pairs.
    for i in range(n):
        for j in range(i + 1, n):
            total_pmi += graph.get_pmi(card_ids[i], card_ids[j])
            
    return total_pmi


def load_corpus() -> List[List[int]]:
    corpus = []
    try:
        with open("logs/kaggle_summary/scraped_decks.json", "r") as f:
            data = json.load(f)
            if "opp_win_decks" in data:
                corpus.extend(data["opp_win_decks"])
            if "us_win_decks" in data:
                corpus.extend(data["us_win_decks"])
    except FileNotFoundError:
        pass
    
    # Try to load iteration_result.json
    try:
        with open("logs/iteration_result.json", "r") as f:
            data = json.load(f)
            # if we have winning decks in iteration_result, we could parse them
            pass
    except FileNotFoundError:
        pass
        
    return corpus

_GLOBAL_GRAPH = None

def get_global_synergy_graph() -> SynergyGraph:
    global _GLOBAL_GRAPH
    if _GLOBAL_GRAPH is None:
        _GLOBAL_GRAPH = SynergyGraph()
        corpus = load_corpus()
        if corpus:
            _GLOBAL_GRAPH.build_from_corpus(corpus)
    return _GLOBAL_GRAPH
