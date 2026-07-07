import logging
from pathlib import Path

logger = logging.getLogger(__name__)

ALLOWED_PACKETS = {
    "opponent_model": {"OpponentModelPacket"},
    "hand_analyst": {"HandAnalystPacket"},
    "turn_planner": {"TurnPlannerPacket"},
    "strategy_agent": {"StrategyPacket"},
    "time_manager": {"TimePacket"},
    "lethal_calculator": {"LethalPacket"}
}

def log_and_flush_delegation(log_file: Path, buffer: list, event_name: str, agent_name: str, packet_type: str):
    """Log delegation to buffer."""
    buffer.append({
        "event": event_name,
        "agent_called": agent_name,
        "packet_type": packet_type
    })
