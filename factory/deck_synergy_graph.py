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

    def get_pmi(self, card_a: int | str, card_b: int | str) -> float:
        try:
            card_a = int(card_a)
            card_b = int(card_b)
        except (ValueError, TypeError):
            return 0.0
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
                if len(comp) > 1:
                    engines.append(comp)
        return engines


from utils.compute_pmi import compute_pmi


from utils.compute_jaccard import compute_jaccard


from utils.score_deck_synergy import score_deck_synergy


from utils.load_corpus import load_corpus

_GLOBAL_GRAPH = None

from utils.get_global_synergy_graph import get_global_synergy_graph
