class OrchestratorStatePublicMixin:
    def get_public_state(self, game_state) -> dict:
        if hasattr(game_state, "my_hand"):
            return {
                "my_hand_count": len(game_state.my_hand),
                "my_deck_count": game_state.my_deck_count,
                "my_prizes": game_state.my_prizes,
                "my_active_pokemon": game_state.my_active_pokemon,
                "my_bench": game_state.my_bench,
                "my_active_damage": game_state.my_active_damage,
                "opponent_active": game_state.opponent_active,
                "opponent_bench_count": len(game_state.opponent_bench),
                "opponent_prizes": game_state.opponent_prizes,
                "opponent_discard": game_state.opponent_discard,
                "turn_number": self.current_turn,
                "legal_attacks": game_state.legal_attacks,
                "legal_attachments": game_state.legal_attachments,
                "legal_bench": game_state.legal_bench,
                "legal_evolutions": game_state.legal_evolutions,
                "legal_trainers": game_state.legal_trainers,
            }
        from agents.schemas import GameState
        gs = GameState.from_dict(game_state)
        return self.get_public_state(gs)
