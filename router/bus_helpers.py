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

from utils.log_and_flush_delegation import log_and_flush_delegation
