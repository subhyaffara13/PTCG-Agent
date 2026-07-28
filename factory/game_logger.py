"""
factory/game_logger.py
Manages logging streams: Action, Reasoning, and Variance.
"""
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from cb_agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class GameLogger(BaseAgent):
    def __init__(self, log_dir: str = "logs", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.action_logs: List[Dict[str, Any]] = []
        self.reasoning_logs: List[Dict[str, Any]] = []
        self.variance_logs: List[Dict[str, Any]] = []
        self.timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    def register_with_bus(self, bus: Any):
        original_dispatch = bus.dispatch
        def wrapped_dispatch(event_name: str, packet: Any) -> Any:
            state_before = getattr(packet, "board_summary", {}) if hasattr(packet, "board_summary") else {}
            response = original_dispatch(event_name, packet)
            state_after = {"status": "dispatched", "response": str(response)}
            self.log_action(
                turn=getattr(packet, "turn", 0) if hasattr(packet, "turn") else 1,
                agent_called=bus.delegation_map.get(event_name, "unknown"),
                action_taken=event_name,
                game_state_before=state_before,
                game_state_after=state_after
            )
            return response
        bus.dispatch = wrapped_dispatch

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("GameLogger does not receive routed packets")

    def log_action(self, turn: int, agent_called: str, action_taken: str, 
                   game_state_before: Dict[str, Any], game_state_after: Dict[str, Any]):
        if os.environ.get("SKIP_GAME_LOGS") == "1" or os.environ.get("FAST_SIM_MODE", "").lower() == "true": return
        self.action_logs.append({
            "turn": turn, "agent_called": agent_called, "action_taken": action_taken,
            "game_state_before": game_state_before, "game_state_after": game_state_after,
            "timestamp": datetime.now().isoformat()
        })

    def log_reasoning(self, turn: int, strategy_active: str, hand_score: float, 
                      strategy_switch_considered: bool, opponent_archetype_confidence: float, 
                      reasoning_chain: str, reasoning_fired: bool, reasoning_outcome: str):
        if os.environ.get("SKIP_GAME_LOGS") == "1" or os.environ.get("FAST_SIM_MODE", "").lower() == "true": return
        self.reasoning_logs.append({
            "turn": turn, "strategy_active": strategy_active, "hand_score": hand_score,
            "strategy_switch_considered": strategy_switch_considered,
            "opponent_archetype_confidence": opponent_archetype_confidence,
            "reasoning_chain": reasoning_chain, "reasoning_fired": reasoning_fired,
            "reasoning_outcome": reasoning_outcome if reasoning_outcome in {"positive", "negative", "neutral"} else "unknown"
        })

    def log_variance(self, turn: int, event_type: str, expected_outcome: str, 
                     actual_outcome: str, impact_score: float):
        if os.environ.get("SKIP_GAME_LOGS") == "1" or os.environ.get("FAST_SIM_MODE", "").lower() == "true": return
        self.variance_logs.append({
            "turn": turn, "event_type": event_type if event_type in {"bad_draw", "coin_flip", "prize_card"} else "coin_flip",
            "expected_outcome": expected_outcome, "actual_outcome": actual_outcome, "impact_score": impact_score
        })

    def save(self, v_player: str, v_opponent: str):
        if os.environ.get("SKIP_GAME_LOGS") == "1" or os.environ.get("FAST_SIM_MODE") == "true":
            self.action_logs.clear(); self.reasoning_logs.clear(); self.variance_logs.clear()
            return
        from factory.game_logger_io import save_log_streams
        save_log_streams(
            self.log_dir, self.timestamp_str, v_player, v_opponent,
            self.action_logs, self.reasoning_logs, self.variance_logs
        )
        self.action_logs.clear(); self.reasoning_logs.clear(); self.variance_logs.clear()
