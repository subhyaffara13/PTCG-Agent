"""
router/bus.py

Enforces the strict information boundaries between agents in the PTCG Agent System.
Provides a central message bus that matches event types and ensures sub-agents
only receive their permitted scoped packets.
"""

import json
import logging
from typing import Dict, Any, Callable
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Scoped Packet Schemas
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HandAnalystPacket:
    hand: list[str]
    deck_remaining: int
    discard: list[str] = None
    board: list[str] = None


@dataclass(frozen=True)
class TurnPlannerPacket:
    hand_score: float
    priority_profile: dict[str, Any]
    top_play: str = ""
    game_state: dict[str, Any] = None
    turn: int = 1

@dataclass(frozen=True)
class StrategyPacket:
    trigger: str
    board_summary: dict[str, Any]

@dataclass(frozen=True)
class TimePacket:
    time_elapsed: float
    time_limit: float

@dataclass(frozen=True)
class OpponentModelPacket:
    turn: int
    newly_played_cards: list[str]
    revealed_active_pokemon: str
    revealed_bench_count: int
    revealed_hand_size: int
    revealed_prizes_remaining: int
    revealed_discard: list[str]
    game_phase: str

@dataclass(frozen=True)
class LethalPacket:
    my_active_damage: int
    opponent_active_hp: int
    legal_attacks: list[str]


class RouterBus:
    def __init__(self, delegation_map: Dict[str, str], log_dir: str = "logs"):
        self.delegation_map = delegation_map
        self.registry: Dict[str, Callable[[Any], Any]] = {}
        self.log_file = Path(log_dir) / "action_log.json"
        self._action_buffer = []  # In-memory buffer for logs
        # Strict mapping of who is allowed to receive what packet class names
        self.allowed_packets: Dict[str, set] = {
            "opponent_model": {"OpponentModelPacket"},
            "hand_analyst": {"HandAnalystPacket"},
            "turn_planner": {"TurnPlannerPacket"},
            "strategy_agent": {"StrategyPacket"},
            "time_manager": {"TimePacket"},
            "lethal_calculator": {"LethalPacket"}
        }

    def register_agent(self, agent_name: str, callback: Callable[[Any], Any], perspective_flag: str = None):
        """
        Registers an agent's receive callback.
        Verifies that agents modeling the opponent are marked with perspective_flag='opponent'.
        """
        if agent_name == "opponent_model" and perspective_flag != "opponent":
            raise ValueError("opponent_model must have perspective_flag='opponent'")
        self.registry[agent_name] = callback

    def dispatch(self, event_name: str, packet: Any) -> Any:
        """
        Dispatches a packet to the agent registered for the given event name,
        validating packet access rules.
        """
        target_agent = self.delegation_map.get(event_name)
        if not target_agent:
            raise ValueError(f"No agent delegated for event: {event_name}")

        callback = self.registry.get(target_agent)
        if not callback:
            raise ValueError(f"No callback registered for agent: {target_agent}")

        # Enforce boundary: Check class name of the packet against target_agent allowances
        packet_class_name = type(packet).__name__
        allowed = self.allowed_packets.get(target_agent, set())
        
        # Safe guard: Ensure agents do not receive the raw orchestrator state itself
        if packet_class_name in ("GameState", "OrchestratorState"):
            raise PermissionError(f"Agent {target_agent} is blocked from receiving full game state!")

        if packet_class_name not in allowed:
            raise PermissionError(
                f"Boundary Violation: Agent '{target_agent}' is not allowed to receive packet of type '{packet_class_name}'"
            )

        logger.debug(f"Routing {packet_class_name} to {target_agent} for event {event_name}")
        
        # Call the delegate
        response = callback(packet)
        
        # Log delegation details to action_log.json
        self._log_delegation(event_name, target_agent, packet_class_name)
        
        return response

    def _log_delegation(self, event_name: str, agent_name: str, packet_type: str):
        """Appends a delegation log entry to the in-memory buffer."""
        log_entry = {
            "event": event_name,
            "agent_called": agent_name,
            "packet_type": packet_type
        }
        self._action_buffer.append(log_entry)

    def flush_logs(self):
        """Write all buffered logs to disk. Called once at end of game."""
        if self._action_buffer:
            try:
                logs = []
                if self.log_file.exists():
                    content = self.log_file.read_text(encoding="utf-8").strip()
                    if content:
                        try:
                            logs = json.loads(content)
                            if not isinstance(logs, list):
                                logs = [logs]
                        except json.JSONDecodeError:
                            logs = []
                logs.extend(self._action_buffer)
                self.log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
                self._action_buffer.clear()
            except Exception as e:
                logger.error(f"Failed to write delegation logs to {self.log_file}: {e}")
            self._action_buffer.clear()
