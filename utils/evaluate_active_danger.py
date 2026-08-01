
def evaluate_active_danger(my_damage: int, opp_hp: int, legal_attacks: list, 
                           opp_active_id, my_hp: int, legal_retreats: list, 
                           my_attached: int = 0, boss_prob: float = 0.0) -> dict:
    """Scan active HP to detect lethal threat and trigger retreat priorities."""
    try:
        from cb_agents.heuristic_pipeline_check import check_lethal
        return check_lethal(
            my_damage=my_damage,
            opp_hp=opp_hp,
            legal_attacks=legal_attacks,
            opp_active_id=opp_active_id,
            my_hp=my_hp,
            legal_retreats=legal_retreats,
            my_attached=my_attached,
            boss_prob=boss_prob
        )
    except Exception as e:
        logger.exception(f"Lethal detection execution failed: {e}")
        return {"action_override": None, "reasoning_chain": f"Lethal detector error: {e}"}


def evaluate_active_danger(my_damage: int, opp_hp: int, legal_attacks: list, 
                           opp_active_id, my_hp: int, legal_retreats: list, 
                           my_attached: int = 0, boss_prob: float = 0.0) -> dict:
    """Scan active HP to detect lethal threat and trigger retreat priorities."""
    try:
        from cb_agents.heuristic_pipeline_check import check_lethal
        return check_lethal(
            my_damage=my_damage,
            opp_hp=opp_hp,
            legal_attacks=legal_attacks,
            opp_active_id=opp_active_id,
            my_hp=my_hp,
            legal_retreats=legal_retreats,
            my_attached=my_attached,
            boss_prob=boss_prob
        )
    except Exception as e:
        logger.exception(f"Lethal detection execution failed: {e}")
        return {"action_override": None, "reasoning_chain": f"Lethal detector error: {e}"}


def evaluate_active_danger(my_damage: int, opp_hp: int, legal_attacks: list, 
                           opp_active_id, my_hp: int, legal_retreats: list, 
                           my_attached: int = 0) -> dict:
    """Scan active HP to detect lethal threat and trigger retreat priorities."""
    try:
        try:
            from cb_agents.heuristic_pipeline_check import check_lethal
        except ImportError:
            from cb_agents.heuristic_pipeline_check import check_lethal
            
        return check_lethal(
            my_damage=my_damage,
            opp_hp=opp_hp,
            legal_attacks=legal_attacks,
            opp_active_id=opp_active_id,
            my_hp=my_hp,
            legal_retreats=legal_retreats,
            my_attached=my_attached
        )
    except Exception as e:
        logger.error(f"Lethal detection execution failed: {e}")
        return {}

