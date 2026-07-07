import time
from router.bus import HandAnalystPacket, TurnPlannerPacket, StrategyPacket, TimePacket, LethalPacket, OpponentModelPacket
from cb_agents.schemas import GameState, BoardSummary
from cb_agents.heuristic_pipeline import pipeline

class OrchestratorRunMixin:
    def _project_opponent_damage(self, game_state) -> int:
        from cb_agents.orchestrator_run_helpers import project_opponent_damage_helper
        return project_opponent_damage_helper(game_state)

    def _check_defensive_retreat(self, game_state, board_summary) -> str:
        from cb_agents.orchestrator_run_helpers import check_defensive_retreat_helper
        return check_defensive_retreat_helper(game_state, board_summary)

    def execute_orchestrator_turn(self, game_state) -> str:
        if self.time_start is None:
            raise RuntimeError("start_game() must be called before first run_turn()")

        def _get_f(obj, k, default=None):
            if isinstance(obj, dict): return obj.get(k, default)
            return getattr(obj, k, default)

        if isinstance(game_state, dict):
            game_state = GameState.from_dict(game_state)
        self.game_state = game_state.__dict__
        self.current_turn += 1
        time_elapsed = time.time() - self.time_start

        from cb_agents.orchestrator_run_helpers import update_opponent_model_helper
        update_opponent_model_helper(self, game_state)

        legal_actions = getattr(game_state, "legal_actions", [])
        if not legal_actions:
            legal_actions = (list(game_state.legal_attacks or []) +
                             list(game_state.legal_retreats or []) +
                             (["pass"] if not game_state.legal_attacks and not game_state.legal_retreats else []))
        legal_actions_list = list(legal_actions)
        active = game_state.opponent_active
        opp_active_id = None
        if active:
            try: opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
            except: pass

        from cb_agents.orchestrator_run_helpers import check_lethal_helper
        lethal_result = check_lethal_helper(game_state)
        if lethal_result.get("action_override") is not None: return lethal_result["action_override"]
        if lethal_result.get("retreat_score_boost"):
            gs_dict = game_state.__dict__ if not isinstance(game_state, dict) else game_state
            gs_dict["retreat_score_boost"] = lethal_result["retreat_score_boost"]
            gs_dict["retreat_target"] = lethal_result.get("retreat_target")

        from cb_agents.orchestrator_run_helpers import handle_time_manager_helper
        time_result_action = handle_time_manager_helper(self, time_elapsed, legal_actions_list, game_state)
        if time_result_action is not None:
            return time_result_action

        hand_result = self.bus.dispatch("HandAnalyst", HandAnalystPacket(
            hand=game_state.my_hand, deck_remaining=game_state.my_deck_count,
            discard=game_state.my_discard, board=game_state.my_board,
            has_searched_deck=game_state.has_searched_deck))

        board_summary = BoardSummary(
            my_prizes_remaining=game_state.my_prizes, opponent_prizes_remaining=game_state.opponent_prizes,
            my_active_hp=game_state.my_active_hp, opponent_active_hp=game_state.opponent_active_hp,
            turn_number=self.current_turn, opponent_archetype=self.opponent_model.identified_archetype,
            opponent_archetype_confidence=self.opponent_model.archetype_confidence,
            bench_has_attacker=game_state.bench_has_attacker, my_bench_count=len(game_state.my_bench),
            prized_probabilities=_get_f(hand_result, "prized_probabilities", {}))

        board_summary_dict = board_summary.__dict__
        board_summary_dict["boss_prob"] = self.belief_tracker.probability_opponent_holds("boss's orders")
        board_summary_dict["iono_prob"] = self.belief_tracker.probability_opponent_holds("iono")

        my_prizes, opponent_prizes = game_state.my_prizes, game_state.opponent_prizes
        trigger = "prize_gap" if (opponent_prizes - my_prizes) >= 2 else "none"
        strategy_result = self.bus.dispatch("StrategyAgent", StrategyPacket(trigger=trigger, board_summary=board_summary_dict))

        gs_dict = game_state.__dict__ if not isinstance(game_state, dict) else game_state
        self.sync_belief_tracker(gs_dict)

        defensive_retreat = self._check_defensive_retreat(game_state, board_summary)
        if defensive_retreat:
            # We override if we are in danger, but strategy agent might have a say.
            # Let's just return it as a defensive override.
            return defensive_retreat

        from cb_agents.sequencing_engine import SequencingEngine
        seq_engine = SequencingEngine()
        legal_actions_list = seq_engine.sequence_actions(legal_actions_list, gs_dict)

        plan_result = self.bus.dispatch("TurnPlanner", TurnPlannerPacket(
            hand_score=_get_f(hand_result, "hand_score", 0), priority_profile=_get_f(strategy_result, "new_strategy"),
            top_play=_get_f(hand_result, "top_play"), game_state=self.get_public_state(game_state),
            turn=self.current_turn, time_remaining=600.0 - time_elapsed))
        return _get_f(plan_result, "primary_action", "pass")
