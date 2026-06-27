import time
from router.bus import HandAnalystPacket, TurnPlannerPacket, StrategyPacket, TimePacket, LethalPacket, OpponentModelPacket
from cb_agents.schemas import GameState, BoardSummary
from cb_agents.heuristic_pipeline import pipeline

class OrchestratorRunMixin:
    def _project_opponent_damage(self, game_state) -> int:
        from cb_agents.card_registry import CardRegistry
        registry = CardRegistry()
        max_dmg = 0
        active = getattr(game_state, 'opponent_active', None)
        if active:
            try:
                opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
                card = registry.get_full_skill(opp_active_id)
                if card:
                    max_dmg = card.damage_output
            except:
                pass
        return max_dmg

    def _check_defensive_retreat(self, game_state, board_summary) -> str:
        opponent_max_damage = self._project_opponent_damage(game_state)
        my_hp = getattr(game_state, 'my_active_hp', 0)
        # Assumed damage is already subtracted from HP in some engines, but let's assume my_active_hp is current HP.
        # If it's max HP, we need to subtract damage. Let's use my_active_hp.
        if opponent_max_damage > 0 and opponent_max_damage >= my_hp:
            retreat_actions = list(getattr(game_state, 'legal_retreats', []))
            if retreat_actions:
                return retreat_actions[0]
        return None

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

        if game_state.opponent_last_play and game_state.opponent_revealed:
            self.bus.dispatch("OpponentModel", OpponentModelPacket(
                turn=self.current_turn, newly_played_cards=game_state.opponent_revealed,
                revealed_active_pokemon=game_state.opponent_active,
                revealed_bench_count=len(game_state.opponent_bench), revealed_hand_size=game_state.opponent_hand_count,
                revealed_prizes_remaining=game_state.opponent_prizes, revealed_discard=game_state.opponent_discard,
                game_phase="early" if self.current_turn < 5 else "mid"))

        arch = self.opponent_model.identified_archetype
        if arch != "unknown" and arch in self.opponent_model.archetypes:
            pool = self.opponent_model.archetypes[arch].get("card_pool", [])
            sig = self.opponent_model.archetypes[arch].get("signature_cards", [])
            new_deck_dict = {}
            for cid in sig:
                try: new_deck_dict[int(cid)] = 4
                except (ValueError, TypeError): pass
            for cid in pool:
                try:
                    cid_int = int(cid)
                    if cid_int not in new_deck_dict: new_deck_dict[cid_int] = 2
                except (ValueError, TypeError): pass
            if new_deck_dict:
                self.belief_tracker.assumed_deck = new_deck_dict

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

        my_active = game_state.my_active_pokemon or {}
        my_attached = len(my_active.get("attached", [])) if isinstance(my_active, dict) else 0

        from cb_agents.card_registry import CardRegistry
        registry = CardRegistry()
        max_damage = 0
        
        my_active_id = None
        if isinstance(my_active, dict):
            my_active_id = my_active.get("id")
        else:
            my_active_id = my_active
            
        if my_active_id is not None and getattr(game_state, "legal_attacks", []):
            try:
                card = registry.get_full_skill(my_active_id)
                if card:
                    max_damage = card.damage_output
            except:
                pass
        
        lethal_result = pipeline.check_lethal(
            my_damage=max_damage, opp_hp=game_state.opponent_active_hp,
            legal_attacks=game_state.legal_attacks, opp_active_id=opp_active_id,
            my_hp=game_state.my_active_hp, legal_retreats=game_state.legal_retreats,
            my_attached=my_attached)
        if lethal_result.get("action_override") is not None: return lethal_result["action_override"]
        if lethal_result.get("retreat_score_boost"):
            gs_dict = game_state.__dict__ if not isinstance(game_state, dict) else game_state
            gs_dict["retreat_score_boost"] = lethal_result["retreat_score_boost"]
            gs_dict["retreat_target"] = lethal_result.get("retreat_target")

        time_result = self.bus.dispatch("TimeManager", TimePacket(
            time_elapsed=time_elapsed, time_limit=600.0, legal_actions=legal_actions_list).__dict__)
        
        t_dir = _get_f(time_result, "directive")
        t_act = _get_f(time_result, "action_override")
        
        if t_dir == "FORCE_PASS":
            if "pass" in legal_actions_list:
                return "pass"
            elif legal_actions_list:
                return legal_actions_list[0]
            else:
                return "pass"
        if t_act is not None: return t_act
        if t_dir == "FAST_MOVE":
            gs_dict = game_state.__dict__ if not isinstance(game_state, dict) else game_state
            best_action, best_score = "pass", -float('inf')
            for a in legal_actions_list:
                s = pipeline.score_action(a, gs_dict)
                if s > best_score:
                    best_score, best_action = s, a
            return best_action

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
