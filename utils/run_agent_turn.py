
def run_agent_turn(orchestrator, observation: dict, deck: list[int]) -> list[int]:
    """Interactions adapter mapping CABT observations to Orchestrator and actions back to options."""
    safe_deck = [x for x in deck] if isinstance(deck, list) else []
    if not isinstance(observation, dict):
        return safe_deck
    select = observation.get("select")
    if select is None: return safe_deck

    options = select.get("options") or select.get("option") or []
    max_count = select.get("maxCount", 1)
    fallback_action = list(range(min(max_count, len(options)))) if options else [0]

    try:
        current = observation.get("current")
        if not current: return fallback_action

        my_idx = current.get("yourIndex", 0)
        players = current.get("players", [])
        if len(players) <= my_idx: return fallback_action

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}


        from factory.game_adapter_state import build_game_state
        game_state = build_game_state(my_state, opp_state, current)

        # Parse legal candidates from options using their exact index in the array
        game_state["legal_attacks"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (12, 13)]
        game_state["legal_attachments"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (8, 9)]
        
        # Load registry for evolution checking
        global _registry
        try:
            if _registry is None:
                from cb_agents.card_registry import CardRegistry
                _registry = CardRegistry(skills_dir=str(orchestrator.skills_dir))
            registry = _registry
        except Exception:
            registry = None

        legal_bench = []
        legal_evolutions = []
        my_hand = game_state.get("my_hand", [])
        for i, opt in enumerate(options):
            if opt.get("type") == 8:
                is_evo = False
                hand_idx = opt.get("index")
                if hand_idx is not None and 0 <= hand_idx < len(my_hand):
                    card_id = my_hand[hand_idx]
                    if registry and card_id:
                        try:
                            card = registry.get_full_skill(card_id)
                            if card:
                                from cb_agents.card_types import CardStage
                                if card.stage in (CardStage.STAGE1, CardStage.STAGE2) or card.previous_stage:
                                    is_evo = True
                        except Exception:
                            pass
                if is_evo:
                    legal_evolutions.append(str(i))
                else:
                    legal_bench.append(str(i))

        game_state["legal_bench"] = legal_bench
        game_state["legal_evolutions"] = legal_evolutions
        game_state["legal_trainers"] = [str(i) for i, opt in enumerate(options) if opt.get("type") == 7]
        game_state["legal_retreats"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (10, 12)]
        game_state["legal_abilities"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (11, 15)]
        game_state["legal_prize_options"] = [str(i) for i, opt in enumerate(options) if opt.get("type") == 2]
        
        sel_type = select.get("type")
        sel_ctx = select.get("context")
        
        game_state["select_prize"] = True if sel_ctx in ("prize", "select_prize") or sel_type == 2 else False
        game_state["select_type"] = sel_type
        game_state["select_context"] = sel_ctx

        # Route only main turn and prize selections to the MCTS engine
        is_main_turn = (sel_type == 0 and sel_ctx == 0)
        is_energy_attach = (sel_type == 7)

        if is_main_turn or game_state["select_prize"]:
            import time
            step_start_time = time.time()
            action_label = orchestrator.run_turn(game_state)
            if time.time() - step_start_time > 1.2:
                logger.warning(f"Step decision took {time.time() - step_start_time:.2f}s (exceeding 1.2s latency guard). Triggering fast fallback.")
                return make_smart_choice(select, observation, fallback_action, str(orchestrator.skills_dir))
            if hasattr(action_label, 'primary_action'):
                action_label = action_label.primary_action

            if is_main_turn and getattr(orchestrator, "last_action", "") != action_label:
                orchestrator.last_action = action_label
                if isinstance(action_label, str) and action_label.startswith("attach_energy:"):
                    parts = action_label.split(":", 2)
                    if len(parts) > 2:
                        orchestrator.last_energy_target = parts[2]
                        
            if is_energy_attach and hasattr(orchestrator, "last_energy_target") and orchestrator.last_energy_target:
                mapped_indices = get_mapped_indices(f"target:{orchestrator.last_energy_target}", options, game_state)
            else:
                mapped_indices = get_mapped_indices(action_label, options, game_state)
                
            if len(mapped_indices) > 1 or (not mapped_indices and action_label != "pass"):
                smart_cand = make_smart_choice(select, observation, fallback_action, str(orchestrator.skills_dir))
                if smart_cand:
                    if mapped_indices:
                        mapped_indices = [idx for idx in smart_cand if idx in mapped_indices] + [idx for idx in smart_cand if idx not in mapped_indices]
                    else:
                        mapped_indices = smart_cand

            if not mapped_indices: mapped_indices = [0]

            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count: break
            return selected
        else:
            return make_smart_choice(select, observation, fallback_action, str(orchestrator.skills_dir))
    except Exception as e:
        logger.error(f"Error resolving agent choice: {e}")
        return fallback_action

