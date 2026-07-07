import json
import logging
from pathlib import Path
from typing import Any

from cb_agents.base_agent import BaseAgent
from cb_agents.mcts_engine import MCTSEngine
from cb_agents.prize_tracker import PrizeTracker
from cb_agents.registry import register_agent
from cb_agents.turn_planner_heuristics import check_mcts_bypass, sort_actions_heuristically
from cb_agents.turn_planner_logging import build_legal_candidates, TurnPlannerLogger
from cb_agents.turn_planner_resolve import resolve_action
from cb_agents.turn_planner_helpers import _process_prize_tracker, _check_lethal_and_update
from router.bus import TurnPlannerPacket

logger = logging.getLogger(__name__)

@register_agent("turn_planner")
class TurnPlanner(BaseAgent):
    def __init__(self, log_dir="logs", skills_dir="skills", perspective_flag="player", shared_context=None, belief_tracker=None):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.shared_context = shared_context
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            self.skills_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create planner directories: {e}")

        try:
            self.rules = (self.shared_context.get_config(str(self.skills_dir), "priority_rules.json")
                          if self.shared_context else self._load_priority_rules())
        except Exception as e:
            logger.error(f"Failed to get_config: {e}")
            self.rules = {"rules": []}
        self.mcts = MCTSEngine(num_simulations=50, belief_tracker=belief_tracker)
        self._logger = TurnPlannerLogger(self.log_dir)
        self._prize_tracker = PrizeTracker()
        self._consecutive_passes = 0

    def _load_priority_rules(self) -> dict:
        path = self.skills_dir / "priority_rules.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read priority_rules.json: {e}")
        return {"rules": []}

    def receive(self, packet: Any) -> dict:
        if isinstance(packet, dict):
            packet = TurnPlannerPacket(**packet)
        if not isinstance(packet, TurnPlannerPacket):
            raise TypeError(f"TurnPlanner received an illegal packet type: {type(packet).__name__}.")
        try:
            game_state = getattr(packet, "game_state", {}) or {}
            turn = getattr(packet, "turn", 1)
            profile = packet.priority_profile
            if profile not in {"aggressive", "defensive", "tempo", "aggro_push", "setup", "disruption", "stall", "closing"}:
                logger.warning(f"Unknown profile '{profile}', falling back to aggro_push")
                profile = "aggro_push"
            game_state["priority_profile"] = profile
            game_state = _process_prize_tracker(game_state, self._prize_tracker, packet)
            game_state["has_searched_deck"] = game_state.get("prize_certainty", 0.0) > 0
            candidates = build_legal_candidates(game_state)
            if self._consecutive_passes >= 10 and "pass" in candidates and len(candidates) > 1:
                logger.warning(f"10-Pass Hard Limit Reached. Forcefully removing 'pass' to break stalemate.")
                candidates.remove("pass")
            time_rem = getattr(packet, "time_remaining", 600.0)
            _check_lethal_and_update(game_state)
            primary, reasoning = resolve_action(candidates, game_state, profile, time_rem, self.mcts, self.rules)
            if primary == "pass":
                self._consecutive_passes += 1
            else:
                self._consecutive_passes = 0
            
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
        except Exception as e:
            logger.error(f"TurnPlanner.receive failed: {e}", exc_info=True)
            return {"action_sequence": ["pass"], "primary_action": "pass", "reasoning_chain": "error_fallback"}

    def get_prize_tracker(self) -> PrizeTracker:
        return self._prize_tracker

    def flush_logs(self):
        try:
            self._logger.flush_logs()
        except Exception as e:
            logger.error(f"flush_logs failed: {e}")
