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
from cb_agents.value_network import PPOPolicyNetwork, PPOValueNetwork
from router.bus import TurnPlannerPacket

logger = logging.getLogger(__name__)

@register_agent("turn_planner")
class TurnPlanner(BaseAgent):
    def __init__(self, log_dir="logs", skills_dir="skills", perspective_flag="player", shared_context=None, belief_tracker=None, model_path=None):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.shared_context = shared_context
        self.model_path = model_path or "models/ppo_actor_critic.pt"
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
        self.mcts = MCTSEngine(
            num_simulations=200, belief_tracker=belief_tracker,
            value_network=PPOValueNetwork(model_path=self.model_path),
            policy_network=PPOPolicyNetwork(model_path=self.model_path)
        )
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
            if turn == 1:
                self._consecutive_passes = 0
            raw_profile = packet.priority_profile
            if isinstance(raw_profile, dict):
                raw_profile = raw_profile.get("strategy") or raw_profile.get("profile") or raw_profile.get("posture") or "aggro_push"
            profile_str = str(raw_profile) if raw_profile else "aggro_push"
            profile_map = {
                "aggressive": "aggro_push",
                "aggro": "aggro_push",
                "prize_race": "aggro_push",
                "aggro_push": "aggro_push",
                "defensive": "stall",
                "stall": "stall",
                "energy_stall": "setup",
                "bench_low": "setup",
                "tempo": "setup",
                "setup": "setup",
                "hand_dead": "setup",
                "control": "disruption",
                "disruption": "disruption",
                "endgame_close": "closing",
                "closing": "closing"
            }
            profile = profile_map.get(profile_str, "aggro_push")
            game_state["priority_profile"] = profile
            game_state = _process_prize_tracker(game_state, self._prize_tracker, packet)
            game_state["has_searched_deck"] = game_state.get("prize_certainty", 0.0) > 0
            # Sync prize certainty to belief tracker for MCTS determinization
            prized_ids = game_state.get("prized_card_ids")
            if prized_ids and self.mcts.belief_tracker:
                self.mcts.belief_tracker.lock_prizes(prized_ids)
            candidates = build_legal_candidates(game_state)
            if self._consecutive_passes >= 10 and "pass" in candidates:
                non_pass = [c for c in candidates if c != "pass"]
                if non_pass:
                    logger.warning(f"10-Pass Hard Limit Reached. Forcefully removing 'pass' to break stalemate.")
                    candidates = non_pass
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
            fallback = "pass"
            current_gs = locals().get("game_state", {}) or {}
            candidates = current_gs.get("legal_actions", []) if isinstance(current_gs, dict) else []
            if isinstance(candidates, list) and candidates:
                fallback = candidates[0]
            return {"action_sequence": [fallback], "primary_action": fallback, "reasoning_chain": "error_fallback"}

    def get_prize_tracker(self) -> PrizeTracker:
        return self._prize_tracker

    def flush_logs(self):
        try:
            self._logger.flush_logs()
        except Exception as e:
            logger.error(f"flush_logs failed: {e}")
