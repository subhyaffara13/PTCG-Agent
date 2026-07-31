"""Shared types for the orchestrator package."""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TurnDecision:
    timing_directive:          str       = "NORMAL"
    time_remaining:            float     = 600.0
    hand_score:                float     = 5.0
    priority_profile:          str       = "aggro_push"
    top_play:                  str       = ""
    strategy:                  str       = "aggro"
    posture:                   str       = "aggressive"
    strategy_confidence:       float     = 1.0
    predicted_opponent_action: str       = "unknown"
    opponent_archetype:        str       = "unknown"
    opponent_confidence:       float     = 0.0
    final_actions:             list[str] = field(default_factory=list)
    action_sequence:           list[str] = field(default_factory=list)
    primary_action:            str       = "PASS"
    reasoning_chain:           str       = ""
    strategy_profile:          str       = "aggro_push"
