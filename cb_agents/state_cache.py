import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)

import hashlib
import json

from utils.board_hash import board_hash

from utils.gs_hash import gs_hash


class CachedEvaluator:
    def __init__(self, evaluator_func):
        self.evaluator_func = evaluator_func
        self.hits = 0
        self.misses = 0
        self._cache: Dict[int, Dict[str, Any]] = {}

    def _eval(self, state_hash: int, **eval_kwargs) -> Dict[str, Any]:
        """Performs an evaluation and tracks cache misses."""
        self.misses += 1
        return self.evaluator_func(**eval_kwargs)

    def evaluate(self, hand_ids: list, board_ids: list, deck_remaining: int, turn: int, **kwargs) -> Dict[str, Any]:
        """Evaluates the board state, returning a cached result if available."""
        h_tuple = tuple(sorted(hand_ids))
        b_tuple = tuple(sorted(board_ids))
        h = board_hash(h_tuple, b_tuple, deck_remaining, turn)

        if h in self._cache:
            self.hits += 1
            return self._cache[h]

        result = self._eval(h, hand_ids=hand_ids, board_ids=board_ids, deck_remaining=deck_remaining, turn=turn, **kwargs)
        self._cache[h] = result
        return result

    def reset(self):
        """Clears the cache."""
        self._cache.clear()
        self.hits = 0
        self.misses = 0

    def get_stats(self) -> Dict[str, int]:
        return {"hits": self.hits, "misses": self.misses}


class TranspositionTable:
    """Simple transposition table for MCTS: maps state hash -> shared node info."""

    def __init__(self):
        self._table: Dict[int, dict] = {}

    def get_or_create(self, gs: dict, make_node) -> tuple:
        """Returns (node, is_hit) for the given game state."""
        h = gs_hash(gs)
        if h == 0:
            n = make_node()
            return n, False
        if h in self._table:
            return self._table[h]["node"], True
        n = make_node()
        self._table[h] = {"node": n, "visits": 0}
        return n, False

    def clear(self):
        self._table.clear()
