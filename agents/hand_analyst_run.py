from typing import Any
from router.bus import HandAnalystPacket
from agents.hand_analyst_prizes import calculate_prized_probabilities
from agents.hand_analyst_metrics import calculate_hand_score_and_profile

def run_hand_analyst(agent, packet: Any) -> dict:
    """Executes hand analysis, tracking prized probabilities and computing scores."""
    if not isinstance(packet, HandAnalystPacket):
        raise TypeError("HandAnalyst got illegal packet type.")

    hand = packet.hand
    deck_remaining = packet.deck_remaining
    turn = getattr(packet, "turn", 1)
    opponent_prizes = getattr(packet, "opponent_prizes_remaining", 6)
    discard = getattr(packet, "discard", []) or []
    board = getattr(packet, "board", []) or []

    prize_remaining, total_unrevealed, prized_probabilities = calculate_prized_probabilities(
        hand, discard, board, agent.deck_base_list, deck_remaining
    )
    
    if prized_probabilities:
        agent._prize_mapper_buffer.append({
            "turn": turn, "perspective": agent.perspective_flag,
            "prize_remaining": prize_remaining, "total_unrevealed": total_unrevealed,
            "prized_probabilities": prized_probabilities
        })

    if not hand:
        response = {
            "hand_score": 0.0, "priority_profile": "stall", "top_play": "none",
            "reasoning_chain": "Empty hand — stall profile activated",
            "prized_probabilities": {}
        }
        agent._log_reasoning(turn, response)
        return response

    response = calculate_hand_score_and_profile(
        hand, board, turn, opponent_prizes, deck_remaining,
        agent.registry, agent.strategy_thresholds, agent.strategy_tips
    )
    response["prized_probabilities"] = prized_probabilities
    agent._log_reasoning(turn, response)
    return response
