"""
tests/test_router_bus.py

Tests boundary enforcement and routing behavior of RouterBus.
"""

import pytest
from router.bus import RouterBus
from cb_agents.opponent_model import OpponentModelPacket

class MockGameState:
    pass

class MockHandAnalystPacket:
    pass

from utils.test_router_boundary_enforcement import test_router_boundary_enforcement
