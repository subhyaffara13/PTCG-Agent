from . import Any, HandAnalyst, RouterBus, TimeManager, TurnPlanner

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

def _step_plan(game_state: dict[str, Any], hand_result: dict[str, Any], strat_result: dict[str, Any], planner: TurnPlanner, router: RouterBus) -> list[dict[str, Any]]:
    from router.bus import TurnPlannerPacket
    priority = strat_result.get("strategy")
    if not priority or priority in ("unknown", "error_fallback"):
        priority = hand_result.get("priority_profile", "balanced")
    return router.dispatch("TurnPlanner", TurnPlannerPacket(
        hand_score=hand_result.get("hand_score", 0.0),
        priority_profile=priority,
        game_state=game_state,
        turn=game_state.get("turn_number", 1),
        time_remaining=game_state.get("time_remaining", 600.0)
    ))

