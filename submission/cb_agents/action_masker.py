import logging
from typing import List, Dict, Tuple
from cb_agents.action_masker_helpers import mask_illegal_actions, calculate_action_signature

logger = logging.getLogger(__name__)


class ActionMasker:
    """
    Filters and groups legal actions before MCTS root expansion.
    """

    def mask_illegal(self, legal_actions: List[str], game_state: dict) -> List[str]:
        """Remove truly invalid or nonsensical actions from the legal actions list."""
        return mask_illegal_actions(legal_actions, game_state)

    def group_isomorphic(self, actions: List[str], game_state: dict) -> Dict[str, List[str]]:
        """Groups structurally equivalent actions into canonical equivalence classes."""
        groups: Dict[str, List[str]] = {}

        bench = game_state.get("my_bench", [])
        bench_signatures: Dict[int, str] = {}
        for i, poke in enumerate(bench):
            if isinstance(poke, dict):
                sig = f"{poke.get('id', '?')}_{poke.get('hp', '?')}_{len(poke.get('attached', []))}"
                bench_signatures[i] = sig
            else:
                bench_signatures[i] = f"unknown_{i}"

        action_sigs: Dict[str, List[str]] = {}
        for action in actions:
            sig = calculate_action_signature(action, bench_signatures, game_state)
            if sig not in action_sigs:
                action_sigs[sig] = []
            action_sigs[sig].append(action)

        for sig, group in action_sigs.items():
            representative = group[0]
            groups[representative] = group

        return groups

    def get_canonical_actions(self, actions: List[str], game_state: dict) -> Tuple[List[str], Dict[str, List[str]]]:
        """Convenience method: filters, groups, and returns canonical representatives."""
        filtered = self.mask_illegal(actions, game_state)
        groups = self.group_isomorphic(filtered, game_state)
        canonical = list(groups.keys())
        return canonical, groups
