"""
router/bus.py
Enforces strict information boundaries between agents in the PTCG Agent System.
"""
import logging
from pathlib import Path
from typing import Dict, Any, Callable
from agents.logging_helper import append_and_flush_logs
from router.bus_helpers import ALLOWED_PACKETS, log_and_flush_delegation

# Re-export packet schemas for backwards compatibility
from router.packets import (  # noqa: F401
    HandAnalystPacket,
    TurnPlannerPacket,
    StrategyPacket,
    TimePacket,
    OpponentModelPacket,
    LethalPacket,
)

logger = logging.getLogger(__name__)

class RouterBus:
    def __init__(self, delegation_map: Dict[str, str], log_dir: str = "logs"):
        self.delegation_map = delegation_map
        self.registry: Dict[str, Callable[[Any], Any]] = {}
        self.log_file = Path(log_dir) / "action_log.json"
        self._action_buffer = []

    def register_agent(self, agent_name: str, callback: Callable[[Any], Any], perspective_flag: str = None):
        if agent_name == "opponent_model" and perspective_flag != "opponent":
            raise ValueError("opponent_model must have perspective_flag='opponent'")
        self.registry[agent_name] = callback

    def dispatch(self, event_name: str, packet: Any) -> Any:
        target_agent = self.delegation_map.get(event_name)
        if not target_agent:
            raise ValueError(f"No agent delegated for event: {event_name}")

        callback = self.registry.get(target_agent)
        if not callback:
            raise ValueError(f"No callback registered for agent: {target_agent}")

        packet_class = type(packet).__name__
        if packet_class in ("GameState", "OrchestratorState"):
            raise PermissionError(f"Agent {target_agent} is blocked from receiving full game state!")

        if packet_class not in ALLOWED_PACKETS.get(target_agent, set()):
            raise PermissionError(f"Boundary Violation: Agent '{target_agent}' cannot receive '{packet_class}'")

        response = callback(packet)
        log_and_flush_delegation(self.log_file, self._action_buffer, event_name, target_agent, packet_class)
        return response

    def flush_logs(self):
        append_and_flush_logs(self.log_file, self._action_buffer)
