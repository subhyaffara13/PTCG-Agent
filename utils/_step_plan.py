from typing import Any

def _step_plan(game_state: dict[str, Any], hand_result: dict[str, Any], strat_result: dict[str, Any], planner: Any, router: Any) -> list[dict[str, Any]]:
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
