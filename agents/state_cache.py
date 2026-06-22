import functools
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)

def board_hash(hand_ids: Tuple[int, ...], board_ids: Tuple[int, ...], deck_remaining: int, turn: int) -> int:
    """Computes a hash for the current board state."""
    return hash((hand_ids, board_ids, deck_remaining, turn))

class CachedEvaluator:
    def __init__(self, evaluator_func):
        self.evaluator_func = evaluator_func
        self.hits = 0
        self.misses = 0
        # Use lru_cache for the actual caching
        self._cached_eval = functools.lru_cache(maxsize=1024)(self._eval)

    def _eval(self, state_hash: int, **kwargs) -> Dict[str, Any]:
        """Wrapper to track cache misses."""
        self.misses += 1
        return self.evaluator_func(**kwargs)

    def evaluate(self, hand_ids: list, board_ids: list, deck_remaining: int, turn: int, **kwargs) -> Dict[str, Any]:
        """Evaluates the board state, returning a cached result if available."""
        h_tuple = tuple(sorted(hand_ids))
        b_tuple = tuple(sorted(board_ids))
        h = board_hash(h_tuple, b_tuple, deck_remaining, turn)
        
        # We can't directly check if it's a hit with lru_cache easily without wrappers,
        # so we track misses inside _eval. If total calls > misses, it was a hit.
        calls_before = self.misses
        result = self._cached_eval(h, hand_ids=hand_ids, board_ids=board_ids, deck_remaining=deck_remaining, turn=turn, **kwargs)
        if self.misses == calls_before:
            self.hits += 1
            
        return result

    def reset(self):
        """Clears the cache."""
        self._cached_eval.cache_clear()
        self.hits = 0
        self.misses = 0
        
    def get_stats(self) -> Dict[str, int]:
        return {"hits": self.hits, "misses": self.misses}
