"""
router/packets.py

Scoped Packet Schemas for strict boundary verification in the PTCG Agent System.
"""

from typing import Any, Dict
from dataclasses import dataclass

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
    opponent_active_id: int = None
    my_active_hp: int = 100
    legal_retreats: list[str] = None
