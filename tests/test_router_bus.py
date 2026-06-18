"""
tests/test_router_bus.py

Tests boundary enforcement and routing behavior of RouterBus.
"""

import pytest
from router.bus import RouterBus
from agents.opponent_model import OpponentModelPacket

class MockGameState:
    pass

class MockHandAnalystPacket:
    pass

def test_router_boundary_enforcement(tmp_path):
    delegation = {
        "on_opponent_play": "opponent_model",
        "turn_start": "hand_analyst"
    }
    bus = RouterBus(delegation, log_dir=str(tmp_path))
    
    # Registration check for opponent model flag
    with pytest.raises(ValueError, match="opponent_model must have perspective_flag='opponent'"):
        bus.register_agent("opponent_model", lambda p: p, perspective_flag="player")

    # Correct registration
    bus.register_agent("opponent_model", lambda p: {"ok": True}, perspective_flag="opponent")
    
    packet = OpponentModelPacket(
        turn=1,
        newly_played_cards=[],
        revealed_active_pokemon=None,
        revealed_bench_count=0,
        revealed_hand_size=5,
        revealed_prizes_remaining=6,
        revealed_discard=[],
        game_phase="early"
    )
    
    res = bus.dispatch("on_opponent_play", packet)
    assert res["ok"] is True

    # Try sending full state or invalid packet
    with pytest.raises(PermissionError, match="Boundary Violation"):
        bus.dispatch("on_opponent_play", MockGameState())

    # Try routing packet not allowed for the recipient
    with pytest.raises(PermissionError, match="Boundary Violation"):
        bus.dispatch("on_opponent_play", MockHandAnalystPacket())
