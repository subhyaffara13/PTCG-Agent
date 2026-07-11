"""
cb_agents/schemas.py
Centralized dataclass definitions for game state and board summaries.
Replaces dict.get() boilerplate across worker files.
"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from cb_agents.schemas_player import PlayerObservation
from cb_agents.schemas_board import BoardSummary


@dataclass
class GameState:
    my_hand: List[int] = field(default_factory=list)
    my_deck_count: int = 60
    my_prizes: int = 6
    my_active_pokemon: Optional[Any] = None
    my_bench: List[Any] = field(default_factory=list)
    my_discard: List[int] = field(default_factory=list)
    my_board: List[int] = field(default_factory=list)
    my_active_damage: int = 0
    my_active_hp: int = 100
    opponent_active: Optional[Any] = None
    opponent_bench: List[Any] = field(default_factory=list)
    opponent_bench_count: int = 0
    opponent_prizes: int = 6
    opponent_discard: List[int] = field(default_factory=list)
    opponent_revealed: List[Any] = field(default_factory=list)
    opponent_last_play: Optional[str] = None
    opponent_hand_count: int = 5
    opponent_deck_count: int = 60
    opponent_active_hp: int = 100
    turn_number: int = 1
    legal_attacks: List[str] = field(default_factory=list)
    legal_attachments: List[str] = field(default_factory=list)
    legal_bench: List[str] = field(default_factory=list)
    legal_evolutions: List[str] = field(default_factory=list)
    legal_trainers: List[str] = field(default_factory=list)
    legal_retreats: List[str] = field(default_factory=list)
    bench_has_attacker: bool = False
    has_searched_deck: bool = False

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "GameState":
        return cls(
            my_hand=d.get("my_hand", []),
            my_deck_count=d.get("my_deck_count", 60),
            my_prizes=d.get("my_prizes", 6),
            my_active_pokemon=d.get("my_active_pokemon"),
            my_bench=d.get("my_bench", []),
            my_discard=d.get("my_discard", []),
            my_board=d.get("my_board", []),
            my_active_damage=d.get("my_active_damage", 0),
            my_active_hp=d.get("my_active_hp", 100),
            opponent_active=d.get("opponent_active"),
            opponent_bench=d.get("opponent_bench", []),
            opponent_bench_count=d.get("opponent_bench_count", 0),
            opponent_prizes=d.get("opponent_prizes", 6),
            opponent_discard=d.get("opponent_discard", []),
            opponent_revealed=d.get("opponent_revealed", []),
            opponent_last_play=d.get("opponent_last_play"),
            opponent_hand_count=d.get("opponent_hand_count", 5),
            opponent_deck_count=d.get("opponent_deck_count", 60),
            opponent_active_hp=d.get("opponent_active_hp", 100),
            turn_number=d.get("turn_number", 1),
            legal_attacks=d.get("legal_attacks", []),
            legal_attachments=d.get("legal_attachments", []),
            legal_bench=d.get("legal_bench", []),
            legal_evolutions=d.get("legal_evolutions", []),
            legal_trainers=d.get("legal_trainers", []),
            legal_retreats=d.get("legal_retreats", []),
            bench_has_attacker=d.get("bench_has_attacker", False),
            has_searched_deck=d.get("has_searched_deck", False),
        )






