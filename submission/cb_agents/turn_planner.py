"""
agents/turn_planner.py

Evaluates the priority rules matching the active hand profile, filters legal actions
against game_state limits, sorts sequences, and outputs action_sequence layouts.
"""

import json
import logging
from pathlib import Path
from typing import Any

from cb_agents.base_agent import BaseAgent
from cb_agents.mcts_engine import MCTSEngine
from cb_agents.registry import register_agent
from cb_agents.turn_planner_heuristics import check_mcts_bypass, sort_actions_heuristically
from cb_agents.turn_planner_logging import build_legal_candidates, TurnPlannerLogger
from router.bus import TurnPlannerPacket

logger = logging.getLogger(__name__)


@register_agent("turn_planner")
class TurnPlanner(BaseAgent):
    def __init__(self, log_dir="logs", skills_dir="skills", perspective_flag="player", shared_context=None):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.shared_context = shared_context
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.rules = (self.shared_context.get_config(str(self.skills_dir), "priority_rules.json")
                      if self.shared_context else self._load_priority_rules())
        self.mcts = MCTSEngine(num_simulations=50)
        self._logger = TurnPlannerLogger(self.log_dir)

    def _load_priority_rules(self) -> dict:
        path = self.skills_dir / "priority_rules.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read priority_rules.json: {e}")
        return {"rules": []}

    def receive(self, packet: Any) -> dict:
        if not isinstance(packet, TurnPlannerPacket):
            raise TypeError(f"TurnPlanner received an illegal packet type: {type(packet).__name__}.")

        game_state = getattr(packet, "game_state", {}) or {}
        turn = getattr(packet, "turn", 1)
        profile = packet.priority_profile
        if profile not in {"aggro_push", "setup", "disruption", "stall", "closing"}:
            profile = "aggro_push"

        candidates = build_legal_candidates(game_state)
        time_rem = getattr(packet, "time_remaining", 600.0)
        primary, reasoning = self._resolve_action(candidates, game_state, profile, time_rem)
        sorted_actions = sort_actions_heuristically(candidates, profile, game_state)

        if primary:
            if primary in sorted_actions:
                sorted_actions.remove(primary)
            sorted_actions.insert(0, primary)
        else:
            primary = sorted_actions[0] if sorted_actions else "pass"
        if not sorted_actions:
            sorted_actions = ["pass"]

        response = {"action_sequence": sorted_actions, "primary_action": primary, "reasoning_chain": reasoning}
        self._logger.log_reasoning(turn, profile, response)
        return response

    def _resolve_action(self, candidates, game_state, profile, time_rem):
        """Run MCTS bypass check then MCTS search. Returns (action, reasoning)."""
        if "my_deck_count" not in game_state:
            return None, ""
        import os
        if os.environ.get("FAST_SIM_MODE") == "true":
            return None, "FAST_SIM_MODE: Heuristic bypass"
        primary = check_mcts_bypass(candidates, game_state, self.rules)
        if primary:
            return primary, f"ELITE SEQUENCING BYPASS: Selected {primary} for max info gain."
            
        # Adaptive simulation count based on remaining turn/match time
        if time_rem > 400.0: sims = 100
        elif time_rem > 200.0: sims = 50
        elif time_rem > 80.0: sims = 25
        else: sims = 10
        
        self.mcts.num_simulations = sims
        primary = self.mcts.search(game_state, candidates)
        return primary, f"MCTS selected {primary} after {sims} sims. Profile: {profile}."

    def flush_logs(self):
        """Write all buffered logs to disk. Called once at end of game."""
        self._logger.flush_logs()
