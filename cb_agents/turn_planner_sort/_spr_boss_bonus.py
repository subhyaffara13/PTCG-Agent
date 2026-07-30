def _score_boss_bonus(action, game_state):
from cb_agents.turn_planner_sort._sort_constants import _PRIORITY_RULES
    bonus = 0
    if _PRIORITY_RULES:
        action_lower = action.lower()
        if action.startswith("play_trainer:") and "boss" in action_lower:
            opp_bench = game_state.get("opponent_bench", [])
            engine_names = {"bibarel", "baxcalibur", "pidgeot", "kirlia", "gardevoir"}
            has_engine = any(
                isinstance(bp, dict) and any(en in str(bp.get("card_name", "")).lower() for en in engine_names)
                for bp in opp_bench
            ) if isinstance(opp_bench, list) else False
            if has_engine:
                bonus -= 20
    return bonus
