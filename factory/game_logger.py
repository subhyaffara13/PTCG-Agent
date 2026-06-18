"""
factory/game_logger.py

Implements GameLogger, managing three parallel logging streams: Action, Reasoning, and Variance.
Inherits from BaseAgent and registers with RouterBus to automatically capture actions.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class GameLogger(BaseAgent):
    def __init__(self, log_dir: str = "logs", perspective_flag: str = "factory"):
        """
        Initializes the GameLogger.
        
        Parameters
        ----------
        log_dir : str
            Directory where log files are written.
        perspective_flag : str
            State perspective ('player', 'opponent', or 'factory').
        """
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # State streams for current game
        self.action_logs: List[Dict[str, Any]] = []
        self.reasoning_logs: List[Dict[str, Any]] = []
        self.variance_logs: List[Dict[str, Any]] = []
        
        # Setup run identifiers
        self.timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    def register_with_bus(self, bus: Any):
        """
        Registers the logger with the RouterBus as a listener/delegation callback hook.
        Every RouterBus delegation event will go through the registered wrapper.
        """
        # Wrap the dispatch function to capture delegations
        original_dispatch = bus.dispatch
        
        def wrapped_dispatch(event_name: str, packet: Any) -> Any:
            state_before = getattr(packet, "board_summary", {}) if hasattr(packet, "board_summary") else {}
            response = original_dispatch(event_name, packet)
            state_after = {"status": "dispatched", "response": str(response)}
            
            # Log action automatically
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
        raise NotImplementedError(
            "GameLogger does not receive routed packets — it records game logs directly"
        )

    def log_action(self, turn: int, agent_called: str, action_taken: str, 
                   game_state_before: Dict[str, Any], game_state_after: Dict[str, Any]):
        """Logs an action taken during a turn."""
        entry = {
            "turn": turn,
            "agent_called": agent_called,
            "action_taken": action_taken,
            "game_state_before": game_state_before,
            "game_state_after": game_state_after,
            "timestamp": datetime.now().isoformat()
        }
        self.action_logs.append(entry)

    def log_reasoning(self, turn: int, strategy_active: str, hand_score: float, 
                      strategy_switch_considered: bool, opponent_archetype_confidence: float, 
                      reasoning_chain: str, reasoning_fired: bool, reasoning_outcome: str):
        """Logs internal agent reasoning state."""
        valid_outcomes = {"positive", "negative", "neutral", "unknown"}
        outcome = reasoning_outcome if reasoning_outcome in valid_outcomes else "unknown"
        
        entry = {
            "turn": turn,
            "strategy_active": strategy_active,
            "hand_score": hand_score,
            "strategy_switch_considered": strategy_switch_considered,
            "opponent_archetype_confidence": opponent_archetype_confidence,
            "reasoning_chain": reasoning_chain,
            "reasoning_fired": reasoning_fired,
            "reasoning_outcome": outcome
        }
        self.reasoning_logs.append(entry)

    def log_variance(self, turn: int, event_type: str, expected_outcome: str, 
                     actual_outcome: str, impact_score: float):
        """Logs variance events."""
        valid_types = {"bad_draw", "coin_flip", "prize_card"}
        e_type = event_type if event_type in valid_types else "coin_flip"
        
        entry = {
            "turn": turn,
            "event_type": e_type,
            "expected_outcome": expected_outcome,
            "actual_outcome": actual_outcome,
            "impact_score": impact_score
        }
        self.variance_logs.append(entry)

    def save(self, v_player: str, v_opponent: str):
        """
        Saves all streams to three separate files per game.
        File format: game_YYYYMMDD_HHMMSS_v{player}_vs_v{opponent}.json
        Suffixes: action, reasoning, variance.
        """
        base_name = f"game_{self.timestamp_str}_v{v_player}_vs_v{v_opponent}"
        
        stream_mappings = {
            "action": self.action_logs,
            "reasoning": self.reasoning_logs,
            "variance": self.variance_logs
        }
        
        for suffix, logs in stream_mappings.items():
            file_path = self.log_dir / f"{suffix}_{base_name}.json"
            
            # Read existing if exists for append safety
            existing_logs = []
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding="utf-8").strip()
                    if content:
                        existing_logs = json.loads(content)
                except Exception as e:
                    logger.error(f"Error reading existing log file {file_path}: {e}")
            
            existing_logs.extend(logs)
            file_path.write_text(json.dumps(existing_logs, indent=2), encoding="utf-8")
        
        # Clear local buffers
        self.action_logs.clear()
        self.reasoning_logs.clear()
        self.variance_logs.clear()
