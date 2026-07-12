class OrchestratorStatePublicMixin:
    def get_public_state(self, game_state) -> dict:
        if not hasattr(game_state, "my_hand"):
            from cb_agents.schemas import GameState
            try:
                game_state = GameState.from_dict(game_state)
            except Exception:
                return {}
            if not hasattr(game_state, "my_hand"):
                return {}
        return {
            "my_hand": list(game_state.my_hand),
            "my_deck_count": game_state.my_deck_count,
            "my_prizes": game_state.my_prizes,
            "my_active_pokemon": game_state.my_active_pokemon,
            "my_bench": list(game_state.my_bench),
            "my_discard": list(game_state.my_discard),
            "my_board": list(game_state.my_board),
            "my_active_damage": game_state.my_active_damage,
            "my_active_hp": game_state.my_active_hp,
            "opponent_active": game_state.opponent_active,
            "opponent_bench": list(game_state.opponent_bench),
            "opponent_bench_count": len(game_state.opponent_bench),
            "opponent_prizes": game_state.opponent_prizes,
            "opponent_discard": list(game_state.opponent_discard),
            "opponent_revealed": list(game_state.opponent_revealed),
            "opponent_last_play": game_state.opponent_last_play,
            "opponent_hand_count": game_state.opponent_hand_count,
            "opponent_deck_count": game_state.opponent_deck_count,
            "opponent_active_hp": game_state.opponent_active_hp,
            "turn_number": self.current_turn,
            "bench_has_attacker": game_state.bench_has_attacker,
            "has_searched_deck": game_state.has_searched_deck,
            "legal_attacks": list(game_state.legal_attacks),
            "legal_attachments": list(game_state.legal_attachments),
            "legal_bench": list(game_state.legal_bench),
            "legal_evolutions": list(game_state.legal_evolutions),
            "legal_trainers": list(game_state.legal_trainers),
            "legal_retreats": list(game_state.legal_retreats),
            "legal_abilities": list(game_state.legal_abilities),
        }
