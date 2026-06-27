from typing import Any
from router.bus import HandAnalystPacket

class HandRunMixin:
    def run_hand_analyst(self, packet: Any) -> dict:
        """Executes hand analysis, tracking prized probabilities and computing scores."""
        if not isinstance(packet, HandAnalystPacket):
            raise TypeError("HandAnalyst got illegal packet type.")

        hand = packet.hand
        deck_remaining = packet.deck_remaining
        turn = getattr(packet, "turn", 1)
        opponent_prizes = getattr(packet, "opponent_prizes_remaining", 6)
        discard = getattr(packet, "discard", []) or []
        board = getattr(packet, "board", []) or []

        has_searched_deck = getattr(packet, "has_searched_deck", False)

        prize_remaining, total_unrevealed, prized_probabilities = self.evaluate_prizes(
            hand, discard, board, self.deck_base_list, deck_remaining,
            has_searched_deck=has_searched_deck
        )
        
        if prized_probabilities:
            self._prize_mapper_buffer.append({
                "turn": turn, "perspective": self.perspective_flag,
                "prize_remaining": prize_remaining, "total_unrevealed": total_unrevealed,
                "prized_probabilities": prized_probabilities
            })

        if not hand:
            response = {
                "hand_score": 0.0, "priority_profile": "stall", "top_play": "none",
                "reasoning_chain": "Empty hand — stall profile activated",
                "prized_probabilities": {}
            }
            self._log_reasoning(turn, response)
            return response

        response = self.calculate_metrics(
            hand, board, turn, opponent_prizes, deck_remaining
        )
        response["prized_probabilities"] = prized_probabilities
        self._log_reasoning(turn, response)
        return response
