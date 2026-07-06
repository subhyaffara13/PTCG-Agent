"""Step helper functions for the Orchestrator."""

from __future__ import annotations
from typing import Any

from router.bus import RouterBus
from agents.hand_analyst   import HandAnalyst
from agents.turn_planner   import TurnPlanner
from agents.time_manager   import TimeManager
from agents.strategy_agent import StrategyAgent
from agents.opponent_model import OpponentModel, OpponentModelPacket
def _step_time(gs: dict[str, Any], timer: TimeManager, router: RouterBus) -> dict[str, Any]:
    from router.bus import TimePacket
    return router.dispatch("TimeManager", TimePacket(
        time_elapsed=gs.get("time_elapsed", 0.0),
        time_limit=gs.get("time_limit", 600.0),
        legal_actions=gs.get("legal_actions", [])
    ))


def _step_hand(gs: dict[str, Any], analyst: HandAnalyst, router: RouterBus) -> dict[str, Any]:
    from router.bus import HandAnalystPacket
    return router.dispatch("HandAnalyst", HandAnalystPacket(
        hand=gs.get("my_hand", []),
        deck_remaining=gs.get("my_deck_count", 60),
    ))


def _step_plan(game_state: dict[str, Any], hand_result: dict[str, Any], planner: TurnPlanner, router: RouterBus) -> list[dict[str, Any]]:
    from router.bus import TurnPlannerPacket
    return router.dispatch("TurnPlanner", TurnPlannerPacket(
        hand_score=hand_result.get("hand_score", 0.0),
        priority_profile=hand_result.get("priority_profile", "balanced"),
        game_state=game_state,
        turn=game_state.get("turn_number", 1),
        time_remaining=game_state.get("time_remaining", 600.0)
    ))


def _step_strategy(gs: dict[str, Any], strategy: StrategyAgent, router: RouterBus) -> dict[str, Any]:
    from router.bus import StrategyPacket
    return router.dispatch("StrategyAgent", StrategyPacket(
        trigger=gs.get("trigger", ""),
        board_summary=gs.get("board_summary", {}),
    ))


def _step_opponent(gs: dict[str, Any], opponent: OpponentModel, router: RouterBus) -> dict[str, Any]:
    active_pokemon = gs.get("opponent_active")
    revealed_active = ""
    if active_pokemon is not None:
        if isinstance(active_pokemon, dict):
            val = active_pokemon.get("id")
            if val is not None:
                revealed_active = str(val)
        else:
            revealed_active = str(active_pokemon)

    opp_pkt = OpponentModelPacket(
        turn                      = int(gs.get("turn_number", 1)),
        newly_played_cards        = gs.get("opponent_revealed", []),
        revealed_active_pokemon   = revealed_active,
        revealed_bench_count      = int(gs.get("opponent_bench_count", 0)),
        revealed_hand_size        = int(gs.get("opponent_hand_size", 0)),
        revealed_prizes_remaining = int(gs.get("opponent_prizes", 6)),
        revealed_discard          = gs.get("opponent_discard", []),
        game_phase                = gs.get("game_phase", "mid"),
    )
    return router.dispatch("OpponentModel", opp_pkt)
