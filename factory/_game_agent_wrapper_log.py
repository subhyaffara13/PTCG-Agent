import logging
logger = logging.getLogger(__name__)

def log_reasoning_and_variance(obs, selected, g_logger, orchestrator):
    current_turn = obs.get("turn_number", 1)
    try:
        strategy_active = getattr(orchestrator.strategy_agent, "current_posture", "tempo")
        last_triggered = getattr(orchestrator.strategy_agent, "last_triggered_turn", 0)
        hand_score = getattr(orchestrator.hand_analyst, "last_hand_score", 5.0)
        opp_confidence = getattr(orchestrator.opponent_model, "archetype_confidence", 0.5)
        g_logger.log_reasoning(turn=current_turn, strategy_active=strategy_active, hand_score=hand_score, strategy_switch_considered=(last_triggered == current_turn), opponent_archetype_confidence=opp_confidence, reasoning_chain=f"Step choice executed. Strategy: {strategy_active}", reasoning_fired=True, reasoning_outcome="positive")
    except Exception as e:
        logger.error(f"Failed to log reasoning: {e}")
    try:
        for log_entry in obs.get("logs", []):
            if log_entry.get("type") in (6, "coin_flip"):
                g_logger.log_variance(turn=current_turn, event_type="coin_flip", expected_outcome="heads", actual_outcome=log_entry.get("result", "heads"), impact_score=0.0)
    except Exception as e:
        logger.error(f"Failed to log variance: {e}")
