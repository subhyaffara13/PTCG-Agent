"""
tests/test_sequencing_rules.py

Unit tests for new sequencing heuristics and prize-aware strategy switching.
"""
import json
import pytest
from cb_agents.turn_planner import TurnPlanner
from cb_agents.strategy_agent import StrategyAgent
from router.bus import TurnPlannerPacket, StrategyPacket
from test_sequencing_rules_helpers import (
    setup_skills_dir, PRIORITY_RULES_EMPTY, STRATEGY_PROFILES_EMPTY, CHARGED_ACTIVE
)

from utils.test_supporter_first_priority import test_supporter_first_priority

from utils.test_energy_over_attachment_prevention import test_energy_over_attachment_prevention

from utils.test_prized_attacker_strategy_switch import test_prized_attacker_strategy_switch
