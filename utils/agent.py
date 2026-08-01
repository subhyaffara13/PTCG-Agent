
def agent(observation, configuration):
    """
    Simple strategic bot that creates units, attacks, and captures.

    Args:
        observation: Kaggle observation struct
        configuration: Kaggle configuration struct

    Returns:
        list of action dicts
    """
    actions = []
    player_idx = observation.player
    player = player_idx + 1
    gold = observation.gold[player_idx]

    units = observation.units if hasattr(observation, "units") else []
    structures = observation.structures if hasattr(observation, "structures") else []
    board = observation.board if hasattr(observation, "board") else []
    map_w = observation.mapWidth if hasattr(observation, "mapWidth") else 20
    map_h = observation.mapHeight if hasattr(observation, "mapHeight") else 20

    # Parse enabled units
    enabled_str = getattr(configuration, "enabledUnits", "W,M,C,A,K,R,S,B")
    enabled_units = set(u.strip() for u in enabled_str.split(",") if u.strip())

    my_units = [u for u in units if u["owner"] == player]
    enemy_units = [u for u in units if u["owner"] != player]
    occupied = {(u["x"], u["y"]) for u in units}

    # ---- Phase 1: Create units ----
    my_buildings = [s for s in structures if s["owner"] == player and s["type"] == "b" and (s["x"], s["y"]) not in occupied]

    for bldg in my_buildings:
        best = None
        for ut in UNIT_PRIORITY:
            if ut in enabled_units and ut in UNIT_COSTS and UNIT_COSTS[ut] <= gold:
                best = ut
                break
        if best:
            actions.append(
                {
                    "type": "create_unit",
                    "unit_type": best,
                    "x": bldg["x"],
                    "y": bldg["y"],
                }
            )
            gold -= UNIT_COSTS[best]
            occupied.add((bldg["x"], bldg["y"]))

    # ---- Phase 2: Unit actions (attack, seize, move) ----
    # Find enemy HQ
    enemy_hq = None
    for s in structures:
        if s["owner"] != player and s["owner"] != 0 and s["type"] == "h":
            enemy_hq = (s["x"], s["y"])
            break

    for unit in my_units:
        if not unit["canMove"] and not unit["canAttack"]:
            continue
        if unit["paralyzedTurns"] > 0:
            continue

        ux, uy = unit["x"], unit["y"]

        # Attack adjacent enemies
        if unit["canAttack"]:
            for enemy in enemy_units:
                dist = abs(ux - enemy["x"]) + abs(uy - enemy["y"])
                attack_range = _get_attack_range(unit["type"])
                if attack_range[0] <= dist <= attack_range[1]:
                    actions.append(
                        {
                            "type": "attack",
                            "from_x": ux,
                            "from_y": uy,
                            "to_x": enemy["x"],
                            "to_y": enemy["y"],
                        }
                    )
                    break  # One attack per unit

        # Seize if on enemy structure
        tile_structure = _get_structure_at(structures, ux, uy)
        if tile_structure and tile_structure["owner"] != player and tile_structure["owner"] != 0:
            actions.append(
                {
                    "type": "seize",
                    "x": ux,
                    "y": uy,
                }
            )
            continue

        # Move toward nearest enemy or enemy HQ
        if unit["canMove"]:
            target = None
            if enemy_units:
                # Find nearest enemy
                nearest = _find_nearest_enemy(ux, uy, enemy_units)
                target = (nearest["x"], nearest["y"])
            elif enemy_hq:
                target = enemy_hq

            if target:
                next_pos = _step_toward(ux, uy, target[0], target[1], board, occupied, map_w, map_h)
                if next_pos and next_pos != (ux, uy):
                    actions.append(
                        {
                            "type": "move",
                            "from_x": ux,
                            "from_y": uy,
                            "to_x": next_pos[0],
                            "to_y": next_pos[1],
                        }
                    )
                    # Update occupied set
                    occupied.discard((ux, uy))
                    occupied.add(next_pos)

    actions.append({"type": "end_turn"})
    return actions

def agent(obs, config):
    if obs.step == 0:
        return [
            721, 721, 722, 722, 722, 722, 723, 723, 723, 723,
            1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219,
            1219, 1219, 1219, 1227, 1227, 1227, 1227, 1262,
            1262, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3
        ]
    return [0]


def agent(observation, configuration=None):
    """
    Main Actuation Agent loop parsed by Kaggle Match runtimes.
    """
    # Safe defaults
    DEFAULT_DECK_FALLBACK = [
        957, 957, 957, 979, 979, 979, 37, 37, 37, 210,
        210, 210, 1121, 1227, 1227, 1227, 1227, 1152, 1152, 1152,
        1152, 1210, 1210, 1210, 1194, 1194, 1194, 1211, 1198, 1256,
        1097, 1097, 1097, 1097, 1182, 1182, 1182, 1182, 1102, 1086,
        1086, 1086, 1086, 1123, 1081, 1122, 6, 6, 6, 6,
        6, 6, 6, 6, 4, 4, 4, 4, 4, 4
    ]
    fallback_action = [0]
    
    try:
        if observation is None:
            return DEFAULT_DECK_FALLBACK
            
        legal_actions = get_val(observation, "legal_actions")
        select = get_val(observation, "select")
        
        # Check if legacy mock unit test is running
        if legal_actions and select is None:
            return [legal_actions[0]]

        # Step 0: If select is None, we must submit the deck (list of 60 integers) at step 0, and [] otherwise
        if select is None:
            if get_val(observation, "step", 0) == 0:
                compile_extension_on_kaggle(configuration)
                # Try to load deck dynamically from Kaggle path first
                loaded_deck = load_deck_on_kaggle(configuration)
                if loaded_deck:
                    return loaded_deck
                # Try to return the global DEFAULT_DECK if it is loaded, otherwise fallback
                try:
                    if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                        return globals()["DEFAULT_DECK"]
                except Exception:
                    pass
                return DEFAULT_DECK_FALLBACK
            return []

        options = get_val(select, "options") or get_val(select, "option") or []
        min_count = get_val(select, "minCount", 1)
        max_count = get_val(select, "maxCount", 1)
        target_count = max(min_count, min(max_count, len(options))) if options else 1
        fallback_action = list(range(min(target_count, len(options)))) if options else [0]

        if "orchestrator" not in globals() or globals()["orchestrator"] is None:
            return fallback_action

        orch = globals()["orchestrator"]

        current = get_val(observation, "current")
        if not current:
            return fallback_action

        # Parse active player state
        my_idx = get_val(current, "yourIndex", 0)
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return fallback_action

        # Dynamically resolve card names for Trainer, Bench and Energy options in hand
        if _registry is not None:
            try:
                from cb_agents.option_resolver import resolve_option_names
                resolve_option_names(options, observation, my_idx, _registry)
            except Exception:
                pass

        def _normalize_pokemon(p):
            if not p or not isinstance(p, dict):
                return p
            p_copy = p.copy()
            attached = []
            energy_cards = p_copy.get("energyCards", [])
            if isinstance(energy_cards, list):
                for ec in energy_cards:
                    if isinstance(ec, dict) and "id" in ec:
                        attached.append(str(ec["id"]))
                    elif isinstance(ec, (int, str)):
                        attached.append(str(ec))
            p_copy["attached"] = attached
            return p_copy

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}

        def _get_active(state):
            val = get_val(state, "active")
            if not val: return None
            if isinstance(val, list): return val[0]
            return val

        # Safely convert CABT board state to simplified game_state dict expected by Orchestrator
        game_state = {
            "my_hand": [get_val(c, "id") for c in get_val(my_state, "hand", []) if c and get_val(c, "id") is not None] if get_val(my_state, "hand") else [],
            "my_deck_count": get_val(my_state, "deckCount", 60),
            "my_prizes": len(get_val(my_state, "prize", [])) if isinstance(get_val(my_state, "prize"), list) else 6,
            "my_active_pokemon": _normalize_pokemon(_get_active(my_state)),
            "my_bench": [_normalize_pokemon(p) for p in get_val(my_state, "bench", [])] if get_val(my_state, "bench") else [],
            
            "opponent_active": _normalize_pokemon(_get_active(opp_state)),
            "opponent_bench": [_normalize_pokemon(p) for p in get_val(opp_state, "bench", [])] if get_val(opp_state, "bench") else [],
            "opponent_bench_count": len(get_val(opp_state, "bench", [])) if get_val(opp_state, "bench") else 0,
            "opponent_prizes": len(get_val(opp_state, "prize", [])) if isinstance(get_val(opp_state, "prize"), list) else 6,
            "opponent_discard": [get_val(c, "id") for c in get_val(opp_state, "discard", []) if c and get_val(c, "id") is not None] if get_val(opp_state, "discard") else [],
            "opponent_deck_count": get_val(opp_state, "deckCount", 60),
            "opponent_revealed": [],
            "opponent_last_play": None,
            
            "turn_number": get_val(current, "turn", 1),
            "time_elapsed": time.time() - _GLOBAL_START_TIME,
            "my_active_hp": 100,
            "opponent_active_hp": 100,
            "bench_has_attacker": False
        }

        # Parse legal candidates from options using exact option index strings (matching game_adapter.py)
        game_state["legal_attacks"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (12, 13, "Attack", "attack")]
        game_state["legal_attachments"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (8, 9, "Attach", "attach", "Energy", "energy")]
        
        legal_bench = []
        legal_evolutions = []
        my_hand = game_state.get("my_hand", [])
        for i, opt in enumerate(options):
            if get_val(opt, "type") in (7, 8, "Play", "play"):
                is_evo = False
                hand_idx = get_val(opt, "index")
                name = get_val(opt, "name", "")
                if hand_idx is not None and isinstance(hand_idx, int) and 0 <= hand_idx < len(my_hand):
                    card_id = my_hand[hand_idx]
                    if _registry and card_id:
                        try:
                            card = _registry.get_full_skill(card_id)
                            if card:
                                from cb_agents.card_types import CardStage
                                if card.stage in (CardStage.STAGE1, CardStage.STAGE2) or card.previous_stage:
                                    is_evo = True
                        except Exception:
                            pass
                elif _registry is not None and name:
                    try:
                        card = _registry.get_full_skill(name)
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
        game_state["legal_trainers"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play", "Trainer", "trainer")]
        game_state["legal_retreats"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (10, 12, "Retreat", "retreat")]
        game_state["legal_abilities"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (9, 11, 15, "Ability", "ability")]

        # Parse detailed active HP if present
        my_active = get_val(my_state, "active")
        if my_active and isinstance(my_active, list) and len(my_active) > 0:
            active_pokemon = my_active[0]
            if active_pokemon:
                game_state["my_active_hp"] = get_val(active_pokemon, "hp", 100)

        opp_active = get_val(opp_state, "active")
        if opp_active and isinstance(opp_active, list) and len(opp_active) > 0:
            active_pokemon = opp_active[0]
            if active_pokemon:
                game_state["opponent_active_hp"] = get_val(active_pokemon, "hp", 100)

        # Check if we are at the Main Turn Menu (SelectType 0, Context 0)
        sel_type = get_val(select, "type")
        sel_ctx = get_val(select, "context")

        if sel_type == 0 and sel_ctx == 0:
            # Call orchestrator to determine action strategy string
            decision = orch.run_turn(game_state)
            action_label = (decision.primary_action.lower() 
                            if hasattr(decision, "primary_action") 
                            else str(decision).lower())

            # Resolve card names into all options dynamically
            if _registry is not None:
                from cb_agents.option_resolver import resolve_option_names
                my_idx = get_val(get_val(observation, "current", {}), "yourIndex", 0)
                resolve_option_names(options, observation, my_idx, _registry)

            # Map orchestrator's prefix action labels to actual select options using get_mapped_indices
            mapped_indices = get_mapped_indices(action_label, options, game_state)

            # If multiple candidate options exist, use smart choice heuristic to rank within those candidates
            if len(mapped_indices) > 1:
                smart_order = make_smart_choice(select, observation, fallback_action)
                # Sort mapped_indices based on smart_order ranking
                mapped_indices.sort(key=lambda idx: smart_order.index(idx) if idx in smart_order else 999)
            # If prefix matching yielded no indices and action is not explicitly PASS,
            # query smart choice over all non-pass legal options first
            if not mapped_indices and action_label != "pass":
                non_pass_opts = [i for i, opt in enumerate(options) if get_val(opt, "type") not in (14, "End", "pass")]
                if non_pass_opts:
                    smart_cand = make_smart_choice(select, observation, fallback_action)
                    if smart_cand:
                        mapped_indices = [idx for idx in smart_cand if idx in non_pass_opts]
                if not mapped_indices:
                    mapped_indices = non_pass_opts

            # If still nothing, or action is explicitly PASS, look for pass/done (Type 14)
            if not mapped_indices or action_label == "pass":
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (14, "End", "pass")]

            if not mapped_indices:
                mapped_indices = [0]

            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
            return selected
        else:
            return make_smart_choice(select, observation, fallback_action)

    except Exception as e:
        import sys
        sys.stderr.write(f"Agent execution crashed internally: {e}\n")
        try:
            _log_action_exception(e)
        except Exception:
            pass
        
        # Determine whether to return fallback deck or fallback action
        try:
            if observation is None or get_val(observation, "select") is None:
                if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                    return globals()["DEFAULT_DECK"]
                return DEFAULT_DECK_FALLBACK
        except Exception:
            pass
        return fallback_action


def agent(observation, configuration=None):
    """
    Main Actuation Agent loop parsed by Kaggle Match runtimes.
    """
    # Safe defaults
    DEFAULT_DECK_FALLBACK = [
        957, 957, 957, 957, 979, 979, 979, 979, 210, 210,
        210, 210, 1121, 1121, 1121, 1121, 1102, 1102, 1102, 1102,
        1213, 1213, 1213, 1213, 1206, 1206, 1206, 1206, 1182, 1182,
        1182, 1182, 1123, 1123, 1123, 1123, 1116, 1116, 1118, 1118,
        1081, 1081, 1097, 1097, 1122, 1122, 6, 6, 6, 6,
        6, 6, 6, 6, 4, 4, 4, 4, 4, 4
    ]
    fallback_action = [0]
    
    try:
        if observation is None:
            return DEFAULT_DECK_FALLBACK
            
        legal_actions = get_val(observation, "legal_actions")
        select = get_val(observation, "select")
        
        # Check if legacy mock unit test is running
        if legal_actions and select is None:
            return [legal_actions[0]]

        # Step 0: If select is None, we must submit the deck (list of 60 integers) at step 0, and [] otherwise
        if select is None:
            if get_val(observation, "step", 0) == 0:
                compile_extension_on_kaggle(configuration)
                # Try to load deck dynamically from Kaggle path first
                loaded_deck = load_deck_on_kaggle(configuration)
                if loaded_deck:
                    return loaded_deck
                # Try to return the global DEFAULT_DECK if it is loaded, otherwise fallback
                try:
                    if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                        return globals()["DEFAULT_DECK"]
                except Exception:
                    pass
                return DEFAULT_DECK_FALLBACK
            return []

        options = get_val(select, "options") or get_val(select, "option") or []
        min_count = get_val(select, "minCount", 1)
        max_count = get_val(select, "maxCount", 1)
        target_count = max(min_count, min(max_count, len(options))) if options else 1
        fallback_action = list(range(min(target_count, len(options)))) if options else [0]

        if "orchestrator" not in globals() or globals()["orchestrator"] is None:
            return fallback_action

        orch = globals()["orchestrator"]

        current = get_val(observation, "current")
        if not current:
            return fallback_action

        # Parse active player state
        my_idx = get_val(current, "yourIndex", 0)
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return fallback_action

        # Dynamically resolve card names for Trainer, Bench and Energy options in hand
        if _registry is not None:
            try:
                from cb_agents.option_resolver import resolve_option_names
                resolve_option_names(options, observation, my_idx, _registry)
            except Exception:
                pass

        def _normalize_pokemon(p):
            if not p or not isinstance(p, dict):
                return p
            p_copy = p.copy()
            attached = []
            energy_cards = p_copy.get("energyCards", [])
            if isinstance(energy_cards, list):
                for ec in energy_cards:
                    if isinstance(ec, dict) and "id" in ec:
                        attached.append(str(ec["id"]))
                    elif isinstance(ec, (int, str)):
                        attached.append(str(ec))
            p_copy["attached"] = attached
            return p_copy

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}

        def _get_active(state):
            val = get_val(state, "active")
            if not val: return None
            if isinstance(val, list): return val[0]
            return val

        # Safely convert CABT board state to simplified game_state dict expected by Orchestrator
        game_state = {
            "my_hand": [get_val(c, "id") for c in get_val(my_state, "hand", []) if c and get_val(c, "id") is not None] if get_val(my_state, "hand") else [],
            "my_deck_count": get_val(my_state, "deckCount", 60),
            "my_prizes": len(get_val(my_state, "prize", [])) if isinstance(get_val(my_state, "prize"), list) else 6,
            "my_active_pokemon": _normalize_pokemon(_get_active(my_state)),
            "my_bench": [_normalize_pokemon(p) for p in get_val(my_state, "bench", [])] if get_val(my_state, "bench") else [],
            
            "opponent_active": _normalize_pokemon(_get_active(opp_state)),
            "opponent_bench": [_normalize_pokemon(p) for p in get_val(opp_state, "bench", [])] if get_val(opp_state, "bench") else [],
            "opponent_bench_count": len(get_val(opp_state, "bench", [])) if get_val(opp_state, "bench") else 0,
            "opponent_prizes": len(get_val(opp_state, "prize", [])) if isinstance(get_val(opp_state, "prize"), list) else 6,
            "opponent_discard": [get_val(c, "id") for c in get_val(opp_state, "discard", []) if c and get_val(c, "id") is not None] if get_val(opp_state, "discard") else [],
            "opponent_deck_count": get_val(opp_state, "deckCount", 60),
            "opponent_revealed": [],
            "opponent_last_play": None,
            
            "turn_number": get_val(current, "turn", 1),
            "time_elapsed": time.time() - _GLOBAL_START_TIME,
            "my_active_hp": 100,
            "opponent_active_hp": 100,
            "bench_has_attacker": False
        }

        # Parse legal candidates from options using exact option index strings (matching game_adapter.py)
        game_state["legal_attacks"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (12, 13, "Attack", "attack")]
        game_state["legal_attachments"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (8, 9, "Attach", "attach", "Energy", "energy")]
        
        legal_bench = []
        legal_evolutions = []
        my_hand = game_state.get("my_hand", [])
        for i, opt in enumerate(options):
            if get_val(opt, "type") in (7, 8, "Play", "play"):
                is_evo = False
                hand_idx = get_val(opt, "index")
                name = get_val(opt, "name", "")
                if hand_idx is not None and isinstance(hand_idx, int) and 0 <= hand_idx < len(my_hand):
                    card_id = my_hand[hand_idx]
                    if _registry and card_id:
                        try:
                            card = _registry.get_full_skill(card_id)
                            if card:
                                from cb_agents.card_types import CardStage
                                if card.stage in (CardStage.STAGE1, CardStage.STAGE2) or card.previous_stage:
                                    is_evo = True
                        except Exception:
                            pass
                elif _registry is not None and name:
                    try:
                        card = _registry.get_full_skill(name)
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
        game_state["legal_trainers"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play", "Trainer", "trainer")]
        game_state["legal_retreats"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (10, 12, "Retreat", "retreat")]
        game_state["legal_abilities"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (9, 11, 15, "Ability", "ability")]

        # Parse detailed active HP if present
        my_active = get_val(my_state, "active")
        if my_active and isinstance(my_active, list) and len(my_active) > 0:
            active_pokemon = my_active[0]
            if active_pokemon:
                game_state["my_active_hp"] = get_val(active_pokemon, "hp", 100)

        opp_active = get_val(opp_state, "active")
        if opp_active and isinstance(opp_active, list) and len(opp_active) > 0:
            active_pokemon = opp_active[0]
            if active_pokemon:
                game_state["opponent_active_hp"] = get_val(active_pokemon, "hp", 100)

        # Check if we are at the Main Turn Menu (SelectType 0, Context 0)
        sel_type = get_val(select, "type")
        sel_ctx = get_val(select, "context")

        if sel_type == 0 and sel_ctx == 0:
            # Call orchestrator to determine action strategy string
            decision = orch.run_turn(game_state)
            action_label = (decision.primary_action.lower() 
                            if hasattr(decision, "primary_action") 
                            else str(decision).lower())

            # Resolve card names into all options dynamically
            if _registry is not None:
                from cb_agents.option_resolver import resolve_option_names
                my_idx = get_val(get_val(observation, "current", {}), "yourIndex", 0)
                resolve_option_names(options, observation, my_idx, _registry)

            # Map orchestrator's prefix action labels to actual select options using get_mapped_indices
            mapped_indices = get_mapped_indices(action_label, options, game_state)

            # If multiple candidate options exist, use smart choice heuristic to rank within those candidates
            if len(mapped_indices) > 1:
                smart_order = make_smart_choice(select, observation, fallback_action)
                # Sort mapped_indices based on smart_order ranking
                mapped_indices.sort(key=lambda idx: smart_order.index(idx) if idx in smart_order else 999)
            # If prefix matching yielded no indices and action is not explicitly PASS,
            # query smart choice over all non-pass legal options first
            if not mapped_indices and action_label != "pass":
                non_pass_opts = [i for i, opt in enumerate(options) if get_val(opt, "type") not in (14, "End", "pass")]
                if non_pass_opts:
                    smart_cand = make_smart_choice(select, observation, fallback_action)
                    if smart_cand:
                        mapped_indices = [idx for idx in smart_cand if idx in non_pass_opts]
                if not mapped_indices:
                    mapped_indices = non_pass_opts

            # If still nothing, or action is explicitly PASS, look for pass/done (Type 14)
            if not mapped_indices or action_label == "pass":
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (14, "End", "pass")]

            if not mapped_indices:
                mapped_indices = [0]

            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
            return selected
        else:
            return make_smart_choice(select, observation, fallback_action)

    except Exception as e:
        import sys
        sys.stderr.write(f"Agent execution crashed internally: {e}\n")
        try:
            _log_action_exception(e)
        except Exception:
            pass
        
        # Determine whether to return fallback deck or fallback action
        try:
            if observation is None or get_val(observation, "select") is None:
                if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                    return globals()["DEFAULT_DECK"]
                return DEFAULT_DECK_FALLBACK
        except Exception:
            pass
        return fallback_action


def agent(observation, configuration=None):
    """
    Main Actuation Agent loop parsed by Kaggle Match runtimes.
    """
    # Safe defaults
    DEFAULT_DECK_FALLBACK = [
        3, 3, 3, 3, 3, 3, 3, 5, 6, 6,
        11, 19, 19, 65, 66, 304, 305, 676, 676, 676,
        676, 677, 678, 722, 723, 741, 742, 743, 878, 879,
        1079, 1081, 1086, 1086, 1086, 1086, 1102, 1115, 1121, 1122,
        1141, 1142, 1145, 1152, 1152, 1152, 1152, 1171, 1182, 1182,
        1182, 1192, 1219, 1225, 1227, 1227, 1227, 1227, 1231, 1255
    ]
    fallback_action = [0]
    
    try:
        if observation is None:
            return DEFAULT_DECK_FALLBACK
            
        legal_actions = get_val(observation, "legal_actions")
        select = get_val(observation, "select")
        
        # Check if legacy mock unit test is running
        if legal_actions and select is None:
            return [legal_actions[0]]

        # Step 0: If select is None, we must submit the deck (list of 60 integers) at step 0, and [] otherwise
        if select is None:
            if get_val(observation, "step", 0) == 0:
                compile_extension_on_kaggle(configuration)
                # Try to return the global DEFAULT_DECK if it is loaded, otherwise fallback
                try:
                    if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                        return globals()["DEFAULT_DECK"]
                except Exception:
                    pass
                return DEFAULT_DECK_FALLBACK
            return []

        options = get_val(select, "option", [])
        max_count = get_val(select, "maxCount", 1)
        fallback_action = list(range(min(max_count, len(options)))) if options else [0]

        if "orchestrator" not in globals() or globals()["orchestrator"] is None:
            return fallback_action

        orch = globals()["orchestrator"]

        current = get_val(observation, "current")
        if not current:
            return fallback_action

        # Parse active player state
        my_idx = get_val(current, "yourIndex", 0)
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return fallback_action

        # Dynamically resolve card names for Trainer, Bench and Energy options in hand
        resolve_option_names(options, observation, my_idx)

        def _normalize_pokemon(p):
            if not p or not isinstance(p, dict):
                return p
            p_copy = p.copy()
            attached = []
            energy_cards = p_copy.get("energyCards", [])
            if isinstance(energy_cards, list):
                for ec in energy_cards:
                    if isinstance(ec, dict) and "id" in ec:
                        attached.append(str(ec["id"]))
                    elif isinstance(ec, (int, str)):
                        attached.append(str(ec))
            p_copy["attached"] = attached
            return p_copy

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}

        # Safely convert CABT board state to simplified game_state dict expected by Orchestrator
        game_state = {
            "my_hand": [get_val(c, "id") for c in get_val(my_state, "hand", []) if c and get_val(c, "id") is not None] if get_val(my_state, "hand") else [],
            "my_deck_count": get_val(my_state, "deckCount", 60),
            "my_prizes": len(get_val(my_state, "prize", [])) if isinstance(get_val(my_state, "prize"), list) else 6,
            "my_active_pokemon": _normalize_pokemon(get_val(my_state, "active", [None])[0]) if get_val(my_state, "active") else None,
            "my_bench": [_normalize_pokemon(p) for p in get_val(my_state, "bench", [])] if get_val(my_state, "bench") else [],
            
            "opponent_active": _normalize_pokemon(get_val(opp_state, "active", [None])[0]) if get_val(opp_state, "active") else None,
            "opponent_bench": [_normalize_pokemon(p) for p in get_val(opp_state, "bench", [])] if get_val(opp_state, "bench") else [],
            "opponent_bench_count": len(get_val(opp_state, "bench", [])) if get_val(opp_state, "bench") else 0,
            "opponent_prizes": len(get_val(opp_state, "prize", [])) if isinstance(get_val(opp_state, "prize"), list) else 6,
            "opponent_discard": [get_val(c, "id") for c in get_val(opp_state, "discard", []) if c and get_val(c, "id") is not None] if get_val(opp_state, "discard") else [],
            "opponent_revealed": [],
            "opponent_last_play": None,
            
            "turn_number": get_val(current, "turn", 1),
            "my_active_hp": 100,
            "opponent_active_hp": 100,
            "bench_has_attacker": False
        }

        # Parse legal candidates from options
        game_state["legal_attacks"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") in (13, "Attack", "attack")]
        game_state["legal_attachments"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") in (9, "Attach", "attach", "Energy", "energy")]
        
        legal_bench = []
        legal_evolutions = []
        for opt in options:
            if get_val(opt, "type") in (8, "Play", "play"):
                name = get_val(opt, "name", "")
                is_evo = False
                if _registry is not None and name:
                    try:
                        card = _registry.get_full_skill(name)
                        if card:
                            from cb_agents.card_types import CardStage
                            if card.stage in (CardStage.STAGE1, CardStage.STAGE2) or card.previous_stage:
                                is_evo = True
                    except Exception:
                        pass
                if is_evo:
                    legal_evolutions.append(name)
                else:
                    legal_bench.append(name)
                    
        game_state["legal_bench"] = legal_bench
        game_state["legal_evolutions"] = legal_evolutions
        game_state["legal_trainers"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") in (7, "Play", "play")]
        game_state["legal_retreats"] = ["retreat"] if any(get_val(opt, "type") in (10, 12, "Retreat", "retreat") for opt in options) else []
        game_state["legal_abilities"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") in (11, 15, "Ability", "ability")]

        # Parse detailed active HP if present
        my_active = get_val(my_state, "active")
        if my_active and isinstance(my_active, list) and len(my_active) > 0:
            active_pokemon = my_active[0]
            if active_pokemon:
                game_state["my_active_hp"] = get_val(active_pokemon, "hp", 100)

        opp_active = get_val(opp_state, "active")
        if opp_active and isinstance(opp_active, list) and len(opp_active) > 0:
            active_pokemon = opp_active[0]
            if active_pokemon:
                game_state["opponent_active_hp"] = get_val(active_pokemon, "hp", 100)

        # Check if we are at the Main Turn Menu (SelectType 0, Context 0)
        sel_type = get_val(select, "type")
        sel_ctx = get_val(select, "context")

        if sel_type == 0 and sel_ctx == 0:
            # Call orchestrator to determine action strategy string
            decision = orch.run_turn(game_state)
            action_label = (decision.primary_action.lower() 
                            if hasattr(decision, "primary_action") 
                            else str(decision).lower())

            # Map orchestrator's prefix action labels to actual select options
            mapped_indices = []
            if action_label.startswith("attack:"):
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (13, "Attack", "attack")]
            elif action_label.startswith("attach_energy:"):
                parts = action_label.split(":")
                energy_name = parts[1] if len(parts) > 1 else ""
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (9, "Attach", "attach", "Energy", "energy") and str(get_val(opt, "name", "")).lower() == energy_name.lower()]
                if not mapped_indices:
                    mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (9, "Attach", "attach", "Energy", "energy")]
            elif action_label.startswith("bench:") or action_label.startswith("evolve:"):
                poke_name = action_label.split(":", 1)[1]
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (8, "Play", "play") and str(get_val(opt, "name", "")).lower() == poke_name.lower()]
                if not mapped_indices:
                    mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (8, "Play", "play")]
            elif action_label.startswith("play_trainer:"):
                trainer_name = action_label.split(":", 1)[1]
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play") and str(get_val(opt, "name", "")).lower() == trainer_name.lower()]
                if not mapped_indices:
                    mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play")]
            elif action_label.startswith("retreat:"):
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (10, 12, "Retreat", "retreat")]
            elif action_label.startswith("ability:"):
                ability_name = action_label.split(":", 1)[1]
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (11, 15, "Ability", "ability") and str(get_val(opt, "name", "")).lower() == ability_name.lower()]
                if not mapped_indices:
                    mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (11, 15, "Ability", "ability")]

            # If no matches, or action is PASS, look for pass/done (Type 14)
            if not mapped_indices or action_label == "pass":
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (14, "End", "pass")]

            # If still nothing, fallback to first index
            if not mapped_indices:
                mapped_indices = [0]

            # Fill selected indices up to max_count
            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
            return selected
        else:
            # Non-main choice (e.g. starting setup, coin flips, Yes/No, card selection from deck)
            # Use smart heuristic selector instead of naive fallback
            return make_smart_choice(select, observation, fallback_action)

    except Exception as e:
        import sys
        sys.stderr.write(f"Agent execution crashed internally: {e}\n")
        try:
            _log_action_exception(e)
        except Exception:
            pass
        
        # Determine whether to return fallback deck or fallback action
        try:
            if observation is None or get_val(observation, "select") is None:
                if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                    return globals()["DEFAULT_DECK"]
                return DEFAULT_DECK_FALLBACK
        except Exception:
            pass
        return fallback_action


def agent(observation, configuration=None):
    """
    Main Actuation Agent loop parsed by Kaggle Match runtimes.
    """
    # Safe defaults
    DEFAULT_DECK_FALLBACK = [
        3, 3, 3, 3, 3, 3, 3, 5, 6, 6,
        11, 19, 19, 65, 66, 304, 305, 676, 676, 676,
        676, 677, 678, 722, 723, 741, 742, 743, 878, 879,
        1079, 1081, 1086, 1086, 1086, 1086, 1102, 1115, 1121, 1122,
        1141, 1142, 1145, 1152, 1152, 1152, 1152, 1171, 1182, 1182,
        1182, 1192, 1219, 1225, 1227, 1227, 1227, 1227, 1231, 1255
    ]
    fallback_action = [0]
    
    try:
        if observation is None:
            return DEFAULT_DECK_FALLBACK
            
        legal_actions = get_val(observation, "legal_actions")
        select = get_val(observation, "select")
        
        # Check if legacy mock unit test is running
        if legal_actions and select is None:
            return [legal_actions[0]]

        # Step 0: If select is None, we must submit the deck (list of 60 integers) at step 0, and [] otherwise
        if select is None:
            if get_val(observation, "step", 0) == 0:
                compile_extension_on_kaggle(configuration)
                # Try to return the global DEFAULT_DECK if it is loaded, otherwise fallback
                try:
                    if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                        return globals()["DEFAULT_DECK"]
                except Exception:
                    pass
                return DEFAULT_DECK_FALLBACK
            return []

        options = get_val(select, "option", [])
        max_count = get_val(select, "maxCount", 1)
        fallback_action = list(range(min(max_count, len(options)))) if options else [0]

        if "orchestrator" not in globals() or globals()["orchestrator"] is None:
            return fallback_action

        orch = globals()["orchestrator"]

        current = get_val(observation, "current")
        if not current:
            return fallback_action

        # Parse active player state
        my_idx = get_val(current, "yourIndex", 0)
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return fallback_action

        # Dynamically resolve card names for Trainer, Bench and Energy options in hand
        resolve_option_names(options, observation, my_idx)

        def _normalize_pokemon(p):
            if not p or not isinstance(p, dict):
                return p
            p_copy = p.copy()
            attached = []
            energy_cards = p_copy.get("energyCards", [])
            if isinstance(energy_cards, list):
                for ec in energy_cards:
                    if isinstance(ec, dict) and "id" in ec:
                        attached.append(str(ec["id"]))
                    elif isinstance(ec, (int, str)):
                        attached.append(str(ec))
            p_copy["attached"] = attached
            return p_copy

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}

        # Safely convert CABT board state to simplified game_state dict expected by Orchestrator
        game_state = {
            "my_hand": [get_val(c, "id") for c in get_val(my_state, "hand", []) if c and get_val(c, "id") is not None] if get_val(my_state, "hand") else [],
            "my_deck_count": get_val(my_state, "deckCount", 60),
            "my_prizes": len(get_val(my_state, "prize", [])) if isinstance(get_val(my_state, "prize"), list) else 6,
            "my_active_pokemon": _normalize_pokemon(get_val(my_state, "active", [None])[0]) if get_val(my_state, "active") else None,
            "my_bench": [_normalize_pokemon(p) for p in get_val(my_state, "bench", [])] if get_val(my_state, "bench") else [],
            
            "opponent_active": _normalize_pokemon(get_val(opp_state, "active", [None])[0]) if get_val(opp_state, "active") else None,
            "opponent_bench": [_normalize_pokemon(p) for p in get_val(opp_state, "bench", [])] if get_val(opp_state, "bench") else [],
            "opponent_bench_count": len(get_val(opp_state, "bench", [])) if get_val(opp_state, "bench") else 0,
            "opponent_prizes": len(get_val(opp_state, "prize", [])) if isinstance(get_val(opp_state, "prize"), list) else 6,
            "opponent_discard": [get_val(c, "id") for c in get_val(opp_state, "discard", []) if c and get_val(c, "id") is not None] if get_val(opp_state, "discard") else [],
            "opponent_revealed": [],
            "opponent_last_play": None,
            
            "turn_number": get_val(current, "turn", 1),
            "my_active_hp": 100,
            "opponent_active_hp": 100,
            "bench_has_attacker": False
        }

        # Parse legal candidates from options
        game_state["legal_attacks"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") in (13, "Attack", "attack")]
        game_state["legal_attachments"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") in (9, "Attach", "attach", "Energy", "energy")]
        
        legal_bench = []
        legal_evolutions = []
        for opt in options:
            if get_val(opt, "type") in (8, "Play", "play"):
                name = get_val(opt, "name", "")
                is_evo = False
                if _registry is not None and name:
                    try:
                        card = _registry.get_full_skill(name)
                        if card:
                            from cb_agents.card_types import CardStage
                            if card.stage in (CardStage.STAGE1, CardStage.STAGE2) or card.previous_stage:
                                is_evo = True
                    except Exception:
                        pass
                if is_evo:
                    legal_evolutions.append(name)
                else:
                    legal_bench.append(name)
                    
        game_state["legal_bench"] = legal_bench
        game_state["legal_evolutions"] = legal_evolutions
        game_state["legal_trainers"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") in (7, "Play", "play")]
        game_state["legal_retreats"] = ["retreat"] if any(get_val(opt, "type") in (10, 12, "Retreat", "retreat") for opt in options) else []
        game_state["legal_abilities"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") in (11, 15, "Ability", "ability")]

        # Parse detailed active HP if present
        my_active = get_val(my_state, "active")
        if my_active and isinstance(my_active, list) and len(my_active) > 0:
            active_pokemon = my_active[0]
            if active_pokemon:
                game_state["my_active_hp"] = get_val(active_pokemon, "hp", 100)

        opp_active = get_val(opp_state, "active")
        if opp_active and isinstance(opp_active, list) and len(opp_active) > 0:
            active_pokemon = opp_active[0]
            if active_pokemon:
                game_state["opponent_active_hp"] = get_val(active_pokemon, "hp", 100)

        # Check if we are at the Main Turn Menu (SelectType 0, Context 0)
        sel_type = get_val(select, "type")
        sel_ctx = get_val(select, "context")

        if sel_type == 0 and sel_ctx == 0:
            # Call orchestrator to determine action strategy string
            decision = orch.run_turn(game_state)
            action_label = (decision.primary_action.lower() 
                            if hasattr(decision, "primary_action") 
                            else str(decision).lower())

            # Map orchestrator's prefix action labels to actual select options
            mapped_indices = []
            if action_label.startswith("attack:"):
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (13, "Attack", "attack")]
            elif action_label.startswith("attach_energy:"):
                parts = action_label.split(":")
                energy_name = parts[1] if len(parts) > 1 else ""
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (9, "Attach", "attach", "Energy", "energy") and str(get_val(opt, "name", "")).lower() == energy_name.lower()]
                if not mapped_indices:
                    mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (9, "Attach", "attach", "Energy", "energy")]
            elif action_label.startswith("bench:") or action_label.startswith("evolve:"):
                poke_name = action_label.split(":", 1)[1]
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (8, "Play", "play") and str(get_val(opt, "name", "")).lower() == poke_name.lower()]
                if not mapped_indices:
                    mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (8, "Play", "play")]
            elif action_label.startswith("play_trainer:"):
                trainer_name = action_label.split(":", 1)[1]
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play") and str(get_val(opt, "name", "")).lower() == trainer_name.lower()]
                if not mapped_indices:
                    mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play")]
            elif action_label.startswith("retreat:"):
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (10, 12, "Retreat", "retreat")]
            elif action_label.startswith("ability:"):
                ability_name = action_label.split(":", 1)[1]
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (11, 15, "Ability", "ability") and str(get_val(opt, "name", "")).lower() == ability_name.lower()]
                if not mapped_indices:
                    mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (11, 15, "Ability", "ability")]

            # If no matches, or action is PASS, look for pass/done (Type 14)
            if not mapped_indices or action_label == "pass":
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (14, "End", "pass")]

            # If still nothing, fallback to first index
            if not mapped_indices:
                mapped_indices = [0]

            # Fill selected indices up to max_count
            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
            return selected
        else:
            # Non-main choice (e.g. starting setup, coin flips, Yes/No, card selection from deck)
            # Use smart heuristic selector instead of naive fallback
            return make_smart_choice(select, observation, fallback_action)

    except Exception as e:
        import sys
        sys.stderr.write(f"Agent execution crashed internally: {e}\n")
        try:
            _log_action_exception(e)
        except Exception:
            pass
        
        # Determine whether to return fallback deck or fallback action
        try:
            if observation is None or get_val(observation, "select") is None:
                if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                    return globals()["DEFAULT_DECK"]
                return DEFAULT_DECK_FALLBACK
        except Exception:
            pass
        return fallback_action


def agent(observation, configuration):
    """Kaggle agent for Game Arena."""
    global _AGENT_OBJECT, _SETUP_COMPLETE

    if not _SETUP_COMPLETE:
        print("--- Performing one-time agent setup... ---")

        # 1. Add the vendored 'lib' directory to Python's search path.
        print("Updating system path with vendored libraries...")
        script_dir = os.path.dirname(configuration["__raw_path__"])
        lib_dir = os.path.join(script_dir, "lib")
        if lib_dir not in sys.path:
            sys.path.insert(0, lib_dir)
        print(f"System path updated. First entry is now: {sys.path[0]}")

        # 2. Now that the path is set, we can import our libraries.
        # pylint: disable=g-import-not-at-top

        from kaggle_environments.envs.werewolf.harness.base import LLMWerewolfAgent
        from kaggle_environments.envs.werewolf.werewolf import LLM_SYSTEM_PROMPT, AgentFactoryWrapper

        if "MODEL_NAME" not in os.environ:
            raise ValueError("MODEL_NAME was not specified as an environment variable. Agent cannot be configured.")

        if "MODEL_PROXY_KEY" not in os.environ:
            raise ValueError(
                "MODEL_PROXY_KEY was not specified as an environment variable. Model proxy cannot function correctly."
            )

        if "MODEL_PROXY_URL" not in os.environ:
            raise ValueError("MODEL_PROXY_URL was not injected. Agent cannot run.")

        _AGENT_OBJECT = AgentFactoryWrapper(
            agent_class=LLMWerewolfAgent,
            model_name=f"openai/{os.environ['MODEL_NAME']}",
            system_prompt=LLM_SYSTEM_PROMPT,
            litellm_model_proxy_kwargs={
                "api_base": f"{os.environ['MODEL_PROXY_URL']}/openapi",
                "api_key": os.environ["MODEL_PROXY_KEY"],
                "reasoning_effort": "high",
            },
        )

        _SETUP_COMPLETE = True
        print("--- Agent setup complete. ---")

    return _AGENT_OBJECT(observation, configuration)


def agent(observation, configuration):
    """
    Random agent that creates a random affordable unit each turn.

    Args:
        observation: Kaggle observation struct with fields:
            - board: 2D array of terrain codes
            - structures: list of structure dicts
            - units: list of unit dicts
            - gold: [p1_gold, p2_gold]
            - player: agent's player index (0 or 1)
            - turnNumber: current turn
            - mapWidth, mapHeight: map dimensions
        configuration: Kaggle configuration struct

    Returns:
        list of action dicts
    """
    actions = []
    player_idx = observation.player
    player = player_idx + 1  # Game uses 1-indexed players
    gold = observation.gold[player_idx]

    # Get units list
    units = observation.units if hasattr(observation, "units") else []
    structures = observation.structures if hasattr(observation, "structures") else []

    # Find buildings we own that are unoccupied
    occupied = {(u["x"], u["y"]) for u in units}
    my_buildings = [s for s in structures if s["owner"] == player and s["type"] == "b" and (s["x"], s["y"]) not in occupied]

    # Parse enabled units from configuration
    enabled_str = getattr(configuration, "enabledUnits", "W,M,C,A,K,R,S,B")
    enabled_units = [u.strip() for u in enabled_str.split(",") if u.strip()]

    # Try to create a random unit at each available building
    for bldg in my_buildings:
        affordable = [ut for ut in enabled_units if ut in UNIT_COSTS and UNIT_COSTS[ut] <= gold]
        if affordable:
            unit_type = random.choice(affordable)
            actions.append(
                {
                    "type": "create_unit",
                    "unit_type": unit_type,
                    "x": bldg["x"],
                    "y": bldg["y"],
                }
            )
            gold -= UNIT_COSTS[unit_type]

    actions.append({"type": "end_turn"})
    return actions


def agent(observation, configuration):
    global game_state

    ### Do not edit ###
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
    else:
        game_state._update(observation["updates"])

    actions = []

    ### AI Code goes down here! ###
    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]
    width, height = game_state.map.width, game_state.map.height

    resource_tiles: list[Cell] = []
    for y in range(height):
        for x in range(width):
            cell = game_state.map.get_cell(x, y)
            if cell.has_resource():
                resource_tiles.append(cell)

    # we iterate over all our units and do something with them
    for unit in player.units:
        if unit.is_worker() and unit.can_act():
            closest_dist = math.inf
            closest_resource_tile = None
            if unit.get_cargo_space_left() > 0:
                # if the unit is a worker and we have space in cargo, lets find the nearest resource tile and try to mine it
                for resource_tile in resource_tiles:
                    if resource_tile.resource.type == Constants.RESOURCE_TYPES.COAL and not player.researched_coal():
                        continue
                    if (
                        resource_tile.resource.type == Constants.RESOURCE_TYPES.URANIUM
                        and not player.researched_uranium()
                    ):
                        continue
                    dist = resource_tile.pos.distance_to(unit.pos)
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_resource_tile = resource_tile
                if closest_resource_tile is not None:
                    actions.append(unit.move(unit.pos.direction_to(closest_resource_tile.pos)))
            else:
                # if unit is a worker and there is no cargo space left, and we have cities, lets return to them
                if len(player.cities) > 0:
                    closest_dist = math.inf
                    closest_city_tile = None
                    for k, city in player.cities.items():
                        for city_tile in city.citytiles:
                            dist = city_tile.pos.distance_to(unit.pos)
                            if dist < closest_dist:
                                closest_dist = dist
                                closest_city_tile = city_tile
                    if closest_city_tile is not None:
                        move_dir = unit.pos.direction_to(closest_city_tile.pos)
                        actions.append(unit.move(move_dir))

    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))

    return actions


def agent(observation, configuration):
    global agent_processes, t, q

    agent_process = agent_processes[observation.player]
    ### Do not edit ###
    if agent_process is None:
        if "__raw_path__" in configuration:
            cwd = os.path.dirname(configuration["__raw_path__"])
        else:
            cwd = os.path.dirname(__file__)
        agent_process = Popen(["java", "Bot"], stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd)
        agent_processes[observation.player] = agent_process
        atexit.register(cleanup_process)

        # following 4 lines from https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python
        q = Queue()
        t = Thread(target=enqueue_output, args=(agent_process.stderr, q))
        t.daemon = True  # thread dies with the program
        t.start()

    # print observations to agent
    import json

    agent_process.stdin.write((json.dumps(observation) + "\n").encode())
    agent_process.stdin.write((json.dumps(configuration) + "\n").encode())
    agent_process.stdin.flush()

    # wait for data written to stdout
    agent1res = (agent_process.stdout.readline()).decode()

    while True:
        try:
            line = q.get_nowait()
        except Empty:
            # no standard error received, break
            break
        else:
            # standard error output received, print it out
            print(line.decode(), file=sys.stderr, end="")

    agent1res = agent1res.strip()
    outputs = agent1res.split(",")
    actions = {}
    for cmd in outputs:
        if cmd != "":
            shipyard_id, action_str = cmd.split(":")
            actions[shipyard_id] = action_str
    return actions


def agent(obs, config):
    board = Board(obs, config)
    me = board.current_player

    me = board.current_player
    turn = board.step
    spawn_cost = board.configuration.spawn_cost
    kore_left = me.kore

    for shipyard in me.shipyards:
        if shipyard.ship_count > 10:
            direction = Direction.from_index(turn % 4)
            action = ShipyardAction.launch_fleet_with_flight_plan(2, direction.to_char())
            shipyard.next_action = action
        elif kore_left > spawn_cost * shipyard.max_spawn:
            action = ShipyardAction.spawn_ships(shipyard.max_spawn)
            shipyard.next_action = action
            kore_left -= spawn_cost * shipyard.max_spawn
        elif kore_left > spawn_cost:
            action = ShipyardAction.spawn_ships(1)
            shipyard.next_action = action
            kore_left -= spawn_cost

    return me.next_actions


def agent(observation, configuration):
    global agent_processes, t, q

    agent_process = agent_processes[observation.player]
    ### Do not edit ###
    if agent_process is None:
        if "__raw_path__" in configuration:
            cwd = os.path.dirname(configuration["__raw_path__"])
        else:
            cwd = os.path.dirname(__file__)
        agent_process = Popen(["node", "dist/Bot.js"], stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd)
        agent_processes[observation.player] = agent_process
        atexit.register(cleanup_process)

        # following 4 lines from https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python
        q = Queue()
        t = Thread(target=enqueue_output, args=(agent_process.stderr, q))
        t.daemon = True  # thread dies with the program
        t.start()

    # print observations to agent
    import json

    agent_process.stdin.write((json.dumps(observation) + "\n").encode())
    agent_process.stdin.write((json.dumps(configuration) + "\n").encode())
    agent_process.stdin.flush()

    # wait for data written to stdout
    agent1res = (agent_process.stdout.readline()).decode()

    while True:
        try:
            line = q.get_nowait()
        except Empty:
            # no standard error received, break
            break
        else:
            # standard error output received, print it out
            print(line.decode(), file=sys.stderr, end="")

    agent1res = agent1res.strip()
    outputs = agent1res.split(",")
    actions = {}
    for cmd in outputs:
        if cmd != "":
            shipyard_id, action_str = cmd.split(":")
            actions[shipyard_id] = action_str
    return actions


def agent(observation, configuration):
    global agent_processes, t, q

    agent_process = agent_processes[observation.player]
    ### Do not edit ###
    if agent_process is None:
        if "__raw_path__" in configuration:
            cwd = os.path.dirname(configuration["__raw_path__"])
        else:
            cwd = os.path.dirname(__file__)
        agent_process = Popen(["node", "dist/MinerBot.js"], stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd)
        agent_processes[observation.player] = agent_process
        atexit.register(cleanup_process)

        # following 4 lines from https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python
        q = Queue()
        t = Thread(target=enqueue_output, args=(agent_process.stderr, q))
        t.daemon = True  # thread dies with the program
        t.start()

    # print observations to agent
    import json

    agent_process.stdin.write((json.dumps(observation) + "\n").encode())
    agent_process.stdin.write((json.dumps(configuration) + "\n").encode())
    agent_process.stdin.flush()

    # wait for data written to stdout
    agent1res = (agent_process.stdout.readline()).decode()

    while True:
        try:
            line = q.get_nowait()
        except Empty:
            # no standard error received, break
            break
        else:
            # standard error output received, print it out
            print(line.decode(), file=sys.stderr, end="")

    agent1res = agent1res.strip()
    outputs = agent1res.split(",")
    actions = {}
    for cmd in outputs:
        if cmd != "":
            shipyard_id, action_str = cmd.split(":")
            actions[shipyard_id] = action_str
    return actions

