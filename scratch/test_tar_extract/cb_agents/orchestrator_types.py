"""Shared types for the orchestrator package."""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TurnDecision:
    timing_directive:          str
    time_remaining:            float
    hand_score:                float
    priority_profile:          str
    top_play:                  str
    strategy:                  str
    posture:                   str
    strategy_confidence:       float
    predicted_opponent_action: str
    opponent_archetype:        str
    opponent_confidence:       float
    final_actions:             list[str] = field(default_factory=list)
    primary_action:            str       = "PASS"
