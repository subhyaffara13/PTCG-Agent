import time
from router.bus import HandAnalystPacket, TurnPlannerPacket, StrategyPacket, TimePacket, LethalPacket, OpponentModelPacket
from cb_agents.orchestrator_belief import sync_belief_tracker
from cb_agents.orchestrator_state_public import get_public_state

def execute_orchestrator_turn(orchestrator, game_state: dict) -> str:
    """Executes a single turn of the Pokémon TCG match by coordinating sub-agents."""
    orchestrator.game_state = game_state
    orchestrator.current_turn += 1
    time_elapsed = time.time() - orchestrator.time_start

    # Update Opponent Model first if opponent revealed new cards
    if game_state.get("opponent_last_play") and game_state.get("opponent_revealed"):
        orchestrator.bus.dispatch("on_opponent_play", OpponentModelPacket(
            turn=orchestrator.current_turn, newly_played_cards=game_state["opponent_revealed"],
            revealed_active_pokemon=game_state.get("opponent_active"),
            revealed_bench_count=len(game_state.get("opponent_bench", [])), revealed_hand_size=game_state.get("opponent_hand_count", 5),
            revealed_prizes_remaining=game_state.get("opponent_prizes", 6), revealed_discard=game_state.get("opponent_discard", []),
            game_phase="early" if orchestrator.current_turn < 5 else "mid"
        ))

    # Dynamically update belief tracker deck when opponent archetype is identified
    arch = orchestrator.opponent_model.identified_archetype
    if arch != "unknown" and arch in orchestrator.opponent_model.archetypes:
        pool = orchestrator.opponent_model.archetypes[arch].get("card_pool", [])
        sig = orchestrator.opponent_model.archetypes[arch].get("signature_cards", [])
        new_deck_dict = {}
        for cid in sig:
            try:
                new_deck_dict[int(cid)] = 4
            except:
                pass
        for cid in pool:
            try:
                cid_int = int(cid)
                if cid_int not in new_deck_dict:
                    new_deck_dict[cid_int] = 2
            except:
                pass
        if new_deck_dict:
            orchestrator.belief_tracker.assumed_deck = new_deck_dict

    time_result = orchestrator.bus.dispatch("always", TimePacket(time_elapsed=time_elapsed, time_limit=600.0))
    if time_result.get("action_override") is not None:
        return time_result["action_override"]

    active = game_state.get("opponent_active")
    opp_active_id = None
    if active:
        try:
            opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
        except:
            pass

    lethal_result = orchestrator.bus.dispatch("before_turn_planner", LethalPacket(
        my_active_damage=game_state.get("my_active_damage", 0),
        opponent_active_hp=game_state.get("opponent_active_hp", 100),
        legal_attacks=game_state.get("legal_attacks", []),
        opponent_active_id=opp_active_id,
        my_active_hp=game_state.get("my_active_hp", 100),
        legal_retreats=game_state.get("legal_retreats", [])
    ))
    if lethal_result.get("action_override") is not None:
        return lethal_result["action_override"]

    hand_result = orchestrator.bus.dispatch("turn_start", HandAnalystPacket(
        hand=game_state.get("my_hand", []), deck_remaining=game_state.get("my_deck_count", 60),
        discard=game_state.get("my_discard", []), board=game_state.get("my_board", [])
    ))

    board_summary = {
        "my_prizes_remaining": game_state.get("my_prizes", 6),
        "opponent_prizes_remaining": game_state.get("opponent_prizes", 6),
        "my_active_hp": game_state.get("my_active_hp", 100),
        "opponent_active_hp": game_state.get("opponent_active_hp", 100),
        "turn_number": orchestrator.current_turn,
        "opponent_archetype": orchestrator.opponent_model.identified_archetype,
        "opponent_archetype_confidence": orchestrator.opponent_model.archetype_confidence,
        "bench_has_attacker": game_state.get("bench_has_attacker", False),
        "my_bench_count": len(game_state.get("my_bench", [])),
        "prized_probabilities": hand_result.get("prized_probabilities", {})
    }
    
    my_prizes, opponent_prizes = game_state.get("my_prizes", 6), game_state.get("opponent_prizes", 6)
    trigger = "prize_gap" if (opponent_prizes - my_prizes) >= 2 else "none"
    
    strategy_result = orchestrator.bus.dispatch("on_trigger", StrategyPacket(trigger=trigger, board_summary=board_summary))
    active_strategy = strategy_result["new_strategy"]

    sync_belief_tracker(orchestrator.belief_tracker, game_state)

    plan_result = orchestrator.bus.dispatch("after_hand_analysis", TurnPlannerPacket(
        hand_score=hand_result["hand_score"], priority_profile=active_strategy,
        top_play=hand_result["top_play"], game_state=get_public_state(game_state, orchestrator.current_turn),
        turn=orchestrator.current_turn, time_remaining=600.0 - time_elapsed
    ))

    return plan_result["primary_action"]
