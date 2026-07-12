"""Step helper functions for the Orchestrator."""

from __future__ import annotations
from typing import Any

from router.bus import RouterBus
from cb_agents.hand_analyst   import HandAnalyst
from cb_agents.turn_planner   import TurnPlanner
from cb_agents.time_manager   import TimeManager
from cb_agents.strategy_agent import StrategyAgent
from cb_agents.opponent_model import OpponentModel, OpponentModelPacket
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


def _step_strategy(gs: dict[str, Any], orchestrator: Any, router: RouterBus) -> dict[str, Any]:
    from router.bus import StrategyPacket
    
    board_summary = gs.get("board_summary")
    if isinstance(board_summary, dict) and board_summary:
        board_summary.setdefault("my_prizes_remaining", board_summary.get("prizes", 6))
        board_summary.setdefault("opponent_prizes_remaining", board_summary.get("opponent_prizes", 6))
        board_summary.setdefault("my_bench_count", board_summary.get("bench_count", 0))
        board_summary.setdefault("opponent_archetype", "unknown")
        board_summary.setdefault("opponent_archetype_confidence", 0.0)
        board_summary.setdefault("my_active_hp", 100)
        board_summary.setdefault("bench_has_attacker", board_summary.get("bench_count", 0) > 0)
        board_summary.setdefault("priority_profile", gs.get("priority_profile", "balanced"))
    if not isinstance(board_summary, dict) or not board_summary:
        my_bench = gs.get("my_bench", [])
        bench_count = len(my_bench) if isinstance(my_bench, list) else 0
        
        my_active = gs.get("my_active_pokemon")
        
        energy_attached = 0
        if isinstance(my_active, dict):
            energy_attached += len(my_active.get("attached", []))
        if isinstance(my_bench, list):
            for p in my_bench:
                if isinstance(p, dict):
                    energy_attached += len(p.get("attached", []))
                    
        hand_score = gs.get("hand_score", 5.0)
        
        boss_prob = 0.0
        iono_prob = 0.0
        if hasattr(orchestrator, "belief_tracker") and orchestrator.belief_tracker:
            boss_prob = orchestrator.belief_tracker.probability_opponent_holds("boss's orders")
            iono_prob = orchestrator.belief_tracker.probability_opponent_holds("iono")
        
        opponent_archetype = "unknown"
        archetype_confidence = 0.0
        if hasattr(orchestrator, "opponent_model"):
            om = orchestrator.opponent_model
            opponent_archetype = getattr(om, "identified_archetype", "unknown")
            archetype_confidence = getattr(om, "archetype_confidence", 0.0)
        
        my_active_hp = 100
        if isinstance(my_active, dict):
            my_active_hp = my_active.get("hp", 100)
        
        bench_has_attacker = bench_count > 0
        
        board_summary = {
            "prizes": gs.get("my_prizes", 6),
            "opponent_prizes": gs.get("opponent_prizes", 6),
            "bench_count": bench_count,
            "hand_score": hand_score,
            "energy_attached": energy_attached,
            "turn_number": gs.get("turn_number", 1),
            "boss_prob": boss_prob,
            "iono_prob": iono_prob,
            "my_prizes_remaining": gs.get("my_prizes", 6),
            "opponent_prizes_remaining": gs.get("opponent_prizes", 6),
            "my_bench_count": bench_count,
            "opponent_archetype": opponent_archetype,
            "opponent_archetype_confidence": archetype_confidence,
            "my_active_hp": my_active_hp,
            "bench_has_attacker": bench_has_attacker,
            "priority_profile": gs.get("priority_profile", "balanced"),
        }
        
    trigger = gs.get("trigger", "")
    if not trigger:
        my_p = int(board_summary.get("prizes", 6))
        opp_p = int(board_summary.get("opponent_prizes", 6))
        trigger = "prize_gap" if (opp_p - my_p) >= 2 else "none"
        
    result = router.dispatch("StrategyAgent", StrategyPacket(
        trigger=trigger,
        board_summary=board_summary,
    ))
    
    try:
        from cb_agents.strategy_helpers import check_should_trigger, select_new_strategy
        strategy_thresholds = gs.get("strategy_thresholds", {})
        last_priority = gs.get("last_priority_profile", None)
        
        should_trigger, sa_config = check_should_trigger(
            board_summary, trigger, last_priority, strategy_thresholds
        )
        if should_trigger:
            new_strategy = select_new_strategy(
                board_summary,
                result.get("strategy", "unknown"),
                sa_config,
            )
            result["strategy"] = new_strategy
    except Exception:
        pass
    
    return result


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
