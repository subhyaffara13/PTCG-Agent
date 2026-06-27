"""Step helper functions for the Orchestrator."""

from __future__ import annotations
from typing import Any

from router.bus import Router
from agents.hand_analyst   import HandAnalyst
from agents.turn_planner   import TurnPlanner
from agents.time_manager   import TimeManager
from agents.strategy_agent import StrategyAgent
from agents.opponent_model import OpponentModel, OpponentModelPacket
def _step_time(gs: dict[str, Any], timer: TimeManager, router: Router) -> dict[str, Any]:
    from router.bus import TimePacket
    return router.dispatch("TimeManager", TimePacket(
        time_elapsed=gs.get("time_elapsed", 0.0),
        time_limit=gs.get("time_limit", 600.0),
        legal_actions=gs.get("legal_actions", [])
    ))


def _step_hand(gs: dict[str, Any], analyst: HandAnalyst, router: Router) -> dict[str, Any]:
    from router.bus import HandAnalystPacket
    return router.dispatch("HandAnalyst", HandAnalystPacket(
        hand=gs.get("hand", []),
        deck_remaining=gs.get("deck_remaining", 0),
    ))


def _step_plan(hand_result: dict[str, Any], planner: TurnPlanner, router: Router) -> list[dict[str, Any]]:
    from router.bus import TurnPlannerPacket
    return router.dispatch("TurnPlanner", TurnPlannerPacket(
        hand_score=hand_result["hand_score"],
        priority_profile=hand_result["priority_profile"],
    ))


def _step_strategy(gs: dict[str, Any], strategy: StrategyAgent, router: Router) -> dict[str, Any]:
    from router.bus import StrategyPacket
    return router.dispatch("StrategyAgent", StrategyPacket(
        trigger=gs.get("trigger", ""),
        board_summary=gs.get("board_summary", {}),
    ))


def _step_opponent(gs: dict[str, Any], opponent: OpponentModel, router: Router) -> dict[str, Any]:
    opp_pkt = OpponentModelPacket(
        turn                      = int(gs.get("turn_number", 1)),
        newly_played_cards        = gs.get("revealed_cards", []),
        revealed_active_pokemon   = gs.get("opponent_active_pokemon"),
        revealed_bench_count      = int(gs.get("opponent_bench_count", 0)),
        revealed_hand_size        = int(gs.get("opponent_hand_size", 0)),
        revealed_prizes_remaining = int(gs.get("opponent_prizes_remaining", 6)),
        revealed_discard          = gs.get("opponent_discard", []),
        game_phase                = gs.get("game_phase", "mid"),
    )
    return router.dispatch("OpponentModel", opp_pkt)
