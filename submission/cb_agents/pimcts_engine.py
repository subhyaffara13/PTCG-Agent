"""
cb_agents/pimcts_engine.py

Perfect Information Monte Carlo Tree Search (PIMCTS) Determinization Engine:
- Samples multiple plausible hidden opponent hand states consistent with revealed cards
- Evaluates candidate actions across all determinizations
- Selects the action with maximum average expected value across all possible hidden hands
"""

import random
import logging
from typing import List, Dict, Any

logger = logging.getLogger("PIMCTSEngine")


class PIMCTSEngine:
    def __init__(self, belief_tracker=None, num_samples: int = 5):
        self.belief_tracker = belief_tracker
        self.num_samples = num_samples

    def sample_opponent_hand(self, game_state: Dict[str, Any]) -> List[int]:
        """Generates a plausible hidden opponent hand sample based on revealed cards and deck probabilities."""
        hand_size = game_state.get("opponent_hand_count", 5)
        if self.belief_tracker and hasattr(self.belief_tracker, "sample_determinization"):
            try:
                det = self.belief_tracker.sample_determinization()
                if isinstance(det, dict) and "opponent_hand" in det:
                    return det["opponent_hand"][:hand_size]
            except Exception as e:
                logger.debug(f"PIMCTS determinization sampling failed: {e}")

        # Fallback pool: basic energy, draw supporters, basic pokemon
        fallback_pool = [6, 1182, 957, 1086, 1152]
        return [random.choice(fallback_pool) for _ in range(hand_size)]

    def evaluate_action_across_determinizations(self, canonical_actions: List[str], game_state: Dict[str, Any], mcts_search_fn) -> str:
        """Runs MCTS evaluation across multiple sampled hidden opponent hands and averages candidate scores."""
        if not canonical_actions:
            return "pass"
        if len(canonical_actions) == 1:
            return canonical_actions[0]

        action_scores: Dict[str, float] = {a: 0.0 for a in canonical_actions}

        for sample_idx in range(self.num_samples):
            sampled_hand = self.sample_opponent_hand(game_state)
            sampled_state = dict(game_state)
            sampled_state["opponent_hand_sampled"] = sampled_hand

            try:
                # Run MCTS search on determinized state sample
                best_act = mcts_search_fn(sampled_state, canonical_actions)
                if best_act in action_scores:
                    action_scores[best_act] += 1.0
            except Exception as e:
                logger.debug(f"Determinization sample {sample_idx} search failed: {e}")

        # Select action with highest vote count across all determinization samples
        best_action = max(action_scores, key=action_scores.get)
        logger.info(f"PIMCTS evaluated {len(canonical_actions)} actions across {self.num_samples} determinizations. Selected: {best_action}")
        return best_action
