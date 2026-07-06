"""
router/packets.py

Scoped Packet Schemas for strict boundary verification in the PTCG Agent System.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class HandAnalystPacket:
    hand: List[str]
    deck_remaining: int
    discard: Optional[List[str]] = None
    board: Optional[List[str]] = None
    has_searched_deck: bool = False


@dataclass(frozen=True)
class TurnPlannerPacket:
    hand_score: float
    priority_profile: Dict[str, Any]
    top_play: str = ""
    game_state: Optional[Dict[str, Any]] = None
    turn: int = 1
    time_remaining: float = 600.0


@dataclass(frozen=True)
class StrategyPacket:
    trigger: str
    board_summary: Dict[str, Any]


@dataclass(frozen=True)
class TimePacket:
    time_elapsed: float
    time_limit: float
    legal_actions: Optional[List[str]] = None


@dataclass(frozen=True)
class OpponentModelPacket:
    turn: int
    newly_played_cards: List[str]
    revealed_bench_count: int
    revealed_hand_size: int
    revealed_prizes_remaining: int
    revealed_discard: List[str]
    game_phase: str
    revealed_active_pokemon: Optional[str] = None


@dataclass(frozen=True)
class LethalPacket:
    my_active_damage: int
    opponent_active_hp: int
    legal_attacks: List[str]
    opponent_active_id: Optional[int] = None
    my_active_hp: int = 100
    legal_retreats: Optional[List[str]] = None
