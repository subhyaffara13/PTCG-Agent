import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)

import hashlib
import json

def board_hash(hand_ids: Tuple[int, ...], board_ids: Tuple[int, ...], deck_remaining: int, turn: int) -> int:
    """Computes a deterministic hash for the current board state."""
    digest = hashlib.md5(f"{hand_ids}|{board_ids}|{deck_remaining}|{turn}".encode()).hexdigest()
    return int(digest, 16)

def gs_hash(game_state: dict) -> int:
    """Compute a deterministic hash for a game state dict for transposition detection."""
    try:
        key_parts = []
        for k in sorted(game_state.keys()):
            if k in ("legal_actions", "turn_ended", "game_over", "winner", "reasoning_chain"):
                continue
            v = game_state[k]
            try:
                json.dumps(v)
                key_parts.append((k, str(v)))
            except (TypeError, ValueError):
                pass
        return int(hashlib.md5(str(tuple(key_parts)).encode()).hexdigest(), 16)
    except Exception:
        return 0


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
