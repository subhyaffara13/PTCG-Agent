import time
from router.bus import HandAnalystPacket, TurnPlannerPacket, StrategyPacket, TimePacket, LethalPacket, OpponentModelPacket
from agents.schemas import GameState, BoardSummary
from agents.heuristic_pipeline import pipeline

class OrchestratorRunMixin:
    def execute_orchestrator_turn(self, game_state) -> str:
        if self.time_start is None:
            raise RuntimeError("start_game() must be called before first run_turn()")

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

        from agents.card_registry import CardRegistry
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
        if time_result.get("directive") == "FORCE_PASS":
            if "pass" in legal_actions_list:
                return "pass"
            elif legal_actions_list:
                return legal_actions_list[0]
            else:
                return "pass"
        if time_result.get("action_override") is not None: return time_result["action_override"]
        if time_result.get("directive") == "FAST_MOVE":
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
            prized_probabilities=hand_result.get("prized_probabilities", {}))

        my_prizes, opponent_prizes = game_state.my_prizes, game_state.opponent_prizes
        trigger = "prize_gap" if (opponent_prizes - my_prizes) >= 2 else "none"
        strategy_result = self.bus.dispatch("StrategyAgent", StrategyPacket(trigger=trigger, board_summary=board_summary.__dict__))

        gs_dict = game_state.__dict__ if not isinstance(game_state, dict) else game_state
        self.sync_belief_tracker(gs_dict)

        plan_result = self.bus.dispatch("TurnPlanner", TurnPlannerPacket(
            hand_score=hand_result["hand_score"], priority_profile=strategy_result["new_strategy"],
            top_play=hand_result["top_play"], game_state=self.get_public_state(game_state),
            turn=self.current_turn, time_remaining=600.0 - time_elapsed))
        return plan_result["primary_action"]
