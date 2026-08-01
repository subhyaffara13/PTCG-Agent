
def make_smart_choice(select, observation, fallback_action):
    global _registry
    try:
        options = get_val(select, "options") or get_val(select, "option") or []
        if not options:
            return fallback_action
            
        max_count = get_val(select, "maxCount", 1)
        sel_type = get_val(select, "type")
        
        # Resolve skills_dir for CardRegistry
        try:
            if _registry is None:
                from cb_agents.card_registry import CardRegistry
                import os
                from pathlib import Path
                agent_dir = str(Path(__file__).parent.resolve()) if "__file__" in globals() and globals()["__file__"] else os.getcwd()
                skills_dir = os.path.join(agent_dir, "skills")
                _registry = CardRegistry(skills_dir=skills_dir)
            registry = _registry
        except Exception:
            registry = None

        if registry is None:
            return fallback_action

        # Detect if this is likely a hand discard choice (cost for trainer or energy discard)
        is_discard = False
        if sel_type in (1, 2, 4):
            try:
                if sel_type == 4 or str(get_val(select, "context", "")).lower() in ("discard", "energy_discard"):
                    is_discard = True
                else:
                    # Check if all options point to cards in our hand
                    current = get_val(observation, "current")
                    my_idx = get_val(current, "yourIndex", 0)
                    players = get_val(current, "players", [])
                    if len(players) > my_idx:
                        my_hand_ids = [get_val(c, "id") for c in get_val(players[my_idx], "hand", []) if c and get_val(c, "id") is not None]
                        
                        option_card_ids = []
                        for opt in options:
                            opt_id = get_val(opt, "id")
                            if opt_id is None:
                                # Resolve coordinate
                                area = get_val(opt, "area")
                                index = get_val(opt, "index")
                                p_idx = get_val(opt, "playerIndex", 0)
                                if p_idx == my_idx and area == 2: # Hand
                                    hand = get_val(players[my_idx], "hand", [])
                                    if len(hand) > index:
                                        opt_id = get_val(hand[index], "id")
                            if opt_id is not None:
                                option_card_ids.append(opt_id)
                        
                        if option_card_ids and all(oid in my_hand_ids for oid in option_card_ids):
                            is_discard = True
            except Exception:
                pass

        def resolve_instance(val):
            if isinstance(val, list):
                return val[0] if len(val) > 0 else None
            return val

        # Collect board Pokemon names for evolution synergy mapping
        board_pokemon_names = set()
        try:
            current = get_val(observation, "current")
            my_idx = get_val(current, "yourIndex", 0)
            players = get_val(current, "players", [])
            if len(players) > my_idx:
                my_state = players[my_idx]
                act = resolve_instance(get_val(my_state, "active"))
                if act:
                    act_name = get_val(act, "name") or get_val(get_val(act, "card"), "name")
                    if act_name: board_pokemon_names.add(str(act_name).lower())
                for b in get_val(my_state, "bench", []):
                    b_resolved = resolve_instance(b)
                    if b_resolved:
                        b_name = get_val(b_resolved, "name") or get_val(get_val(b_resolved, "card"), "name")
                        if b_name: board_pokemon_names.add(str(b_name).lower())
        except Exception:
            pass

        # Score each option
        scored_options = []
        for idx, opt in enumerate(options):
            card_id = get_val(opt, "id")
            card_name = get_val(opt, "name", "")
            
            # If coordinates are present instead of name/id, resolve them
            if card_id is None and not card_name:
                try:
                    area = get_val(opt, "area")
                    index = get_val(opt, "index")
                    p_idx = get_val(opt, "playerIndex", 0)
                    current = get_val(observation, "current")
                    players = get_val(current, "players", [])
                    if len(players) > p_idx:
                        p_state = players[p_idx]
                        if area == 2: # Hand
                            hand = get_val(p_state, "hand", [])
                            if len(hand) > index:
                                card_id = get_val(hand[index], "id")
                        elif area == 12: # Bench
                            bench = get_val(p_state, "bench", [])
                            if len(bench) > index:
                                bench_item = resolve_instance(bench[index])
                                if bench_item is not None:
                                    card_id = get_val(bench_item, "id")
                        elif area == 4: # Active
                            active = get_val(p_state, "active", [])
                            if len(active) > index:
                                active_item = resolve_instance(active[index])
                                if active_item is not None:
                                    card_id = get_val(active_item, "id")
                except Exception:
                    pass

            card = None
            if card_id is not None:
                card = registry.get_full_skill(card_id)
            if card is None and card_name:
                card = registry.get_full_skill(card_name)
                
            score = 0.0
            if card:
                score = getattr(card, "utility_score", 0.0)
                
                # 1. Boost based on learned rules from Kaggle champions
                card_id_int = getattr(card, "card_id", None)
                if card_id_int is not None:
                    dos_set = getattr(registry, "_learned_dos_set", None)
                    if dos_set is None and hasattr(registry, "learned_dos"):
                        dos_data = getattr(registry, "learned_dos", {})
                        if isinstance(dos_data, dict):
                            dos_list = dos_data.get("deck_dos", [])
                            dos_set = {int(x.get("card_id")) for x in dos_list if isinstance(x, dict) and "card_id" in x}
                        else:
                            dos_set = set()
                        setattr(registry, "_learned_dos_set", dos_set)
                    donts_set = getattr(registry, "_learned_donts_set", None)
                    if donts_set is None and hasattr(registry, "learned_donts"):
                        donts_data = getattr(registry, "learned_donts", {})
                        if isinstance(donts_data, dict):
                            donts_list = donts_data.get("deck_donts", [])
                            donts_set = {int(x.get("card_id")) for x in donts_list if isinstance(x, dict) and "card_id" in x}
                        else:
                            donts_set = set()
                        setattr(registry, "_learned_donts_set", donts_set)

                    if dos_set and int(card_id_int) in dos_set:
                        score += 12.0
                    if donts_set and int(card_id_int) in donts_set:
                        score -= 12.0
                
                # 2. Boost if evolution predecessor is on board
                predecessor = registry.get_evolution_predecessor(getattr(card, "card_name", ""))
                if predecessor and predecessor.lower() in board_pokemon_names:
                    score += 15.0

                # 3. Energy Requirement / Active priority boost
                if sel_type in (1, 4) or str(get_val(select, "context", "")).lower() in ("energy", "attach"):
                    try:
                        area = get_val(opt, "area")
                        index = get_val(opt, "index")
                        p_idx = get_val(opt, "playerIndex", 0)
                        current = get_val(observation, "current")
                        my_idx = get_val(current, "yourIndex", 0)
                        if p_idx == my_idx:
                            players = get_val(current, "players", [])
                            my_state = players[my_idx]
                            instance = None
                            if area == 4: # Active
                                instance = resolve_instance(get_val(my_state, "active"))
                            elif area in (5, 12): # Bench
                                bench = get_val(my_state, "bench", [])
                                if len(bench) > index:
                                    instance = resolve_instance(bench[index])
                            if instance:
                                attached = get_val(instance, "attached", [])
                                attached_count = len(attached) if isinstance(attached, list) else 0
                                required = getattr(card, "energy_cost", 0)
                                if attached_count < required:
                                    # Avoid attaching energy to low-HP or non-attacking support/setup Pokemon
                                    target_name = ""
                                    target_id = get_val(instance, "id")
                                    if target_id is not None and registry:
                                        target_card = registry.get_full_skill(target_id)
                                        if target_card:
                                            target_name = getattr(target_card, "card_name", "").lower()
                                    
                                    is_passive_support = any(s in target_name for s in {"dunsparce", "bidoof", "snom", "remoraid", "jirachi", "manaphy"})
                                    target_hp = get_val(instance, "hp", 100)
                                    target_max_hp = get_val(instance, "maxHp", 100)
                                    is_low_hp = target_hp <= 40 and target_max_hp <= 130
                                    
                                    if is_passive_support or is_low_hp:
                                        boost = -15.0
                                    else:
                                        boost = 10.0 * (required - attached_count)
                                        if area == 4:
                                            boost += 5.0
                                    score += boost
                    except Exception:
                        pass
                
                # 4. Support Pokemon early match boost
                try:
                    current = get_val(observation, "current")
                    turn = get_val(current, "turn", 1)
                    if turn <= 5:
                        support_names = {"bidoof", "bibarel", "snom", "frosmoth", "remoraid", "octillery", "dunsparce", "jirachi", "manaphy", "mew"}
                        card_name_lower = getattr(card, "card_name", "").lower()
                        if any(s in card_name_lower for s in support_names):
                            score += 15.0
                except Exception:
                    pass
                
                if sel_type == 3:
                    score += getattr(card, "ev_score", 0.0) + (getattr(card, "damage_output", 0) * 0.01)
            scored_options.append((idx, score))

        # Value Network One-Step Lookahead Rescoring
        orch = globals().get("orchestrator")
        value_net = getattr(getattr(orch, "mcts", None), "value_network", None) if orch else None
        if value_net:
            try:
                import sys
                current_obs = get_val(observation, "current")
                players_list = get_val(current_obs, "players", [])
                my_idx_val = get_val(current_obs, "yourIndex", 0)
                my_state_dict = players_list[my_idx_val] if len(players_list) > my_idx_val else {}
                choice_ctx = str(get_val(select, "context", "")).lower()
                for i in range(len(scored_options)):
                    idx, base_score = scored_options[i]
                    opt = options[idx]
                    cid = get_val(opt, "id")
                    hyp_state = my_state_dict.copy() if isinstance(my_state_dict, dict) else {}
                    if is_discard and cid is not None:
                        cid_str = str(cid)
                        if cid_str in hyp_state.get("my_hand", []):
                            hand_copy = list(hyp_state["my_hand"])
                            hand_copy.remove(cid_str)
                            hyp_state["my_hand"] = hand_copy
                    elif (choice_ctx in ("draw", "search", "take")) and cid is not None:
                        cid_str = str(cid)
                        hand_copy = list(hyp_state.get("my_hand", []))
                        hand_copy.append(cid_str)
                        hyp_state["my_hand"] = hand_copy
                    
                    val_score = value_net.evaluate(hyp_state)
                    scored_options[i] = (idx, base_score + 10.0 * val_score)
            except Exception as val_err:
                import sys
                sys.stderr.write(f"[smart_choice] Value net evaluation failed: {val_err}\n")

        # Context-aware rescoring for discards: learned_dos +12 dominates utility (0-0.86)
        # so trainers always outscore Pokemon — but Pokemon win the game. Fix the balance.
        if is_discard:
            try:
                current = get_val(observation, "current")
                my_idx = get_val(current, "yourIndex", 0)
                players = get_val(current, "players", [])
                my_state = players[my_idx] if len(players) > my_idx else {}
                bench_slots = len(get_val(my_state, "bench", []))
                active_poke = get_val(my_state, "active", None)
                has_active = bool(active_poke and len(active_poke) > 0 and active_poke[0])
                my_hand = get_val(my_state, "hand", [])
                hand_ids = [get_val(c, "id") for c in my_hand if c]
                for i in range(len(scored_options)):
                    idx, base_score = scored_options[i]
                    opt = options[idx]
                    cid = get_val(opt, "id")
                    if cid is None:
                        area = get_val(opt, "area")
                        index = get_val(opt, "index")
                        if area == 2 and len(my_hand) > index:
                            cid = get_val(my_hand[index], "id")
                    if cid is not None:
                        card = registry.get_full_skill(cid)
                        if card:
                            ct = getattr(card, "card_type", None)
                            ct_name = ct.name if ct else ""
                            card_id_int = int(cid) if not isinstance(cid, int) else cid
                            if ct_name == "POKEMON":
                                count_in_hand = sum(1 for hid in hand_ids if str(hid) == str(cid))
                                is_last_copy = count_in_hand <= 1
                                bench_needed = (6 - bench_slots) if has_active else (6 - bench_slots - 1)
                                if bench_needed > 0 and is_last_copy:
                                    base_score += 25.0  # Strong survival bonus for last Pokemon copy
                                elif bench_needed > 0:
                                    base_score += 10.0
                            elif ct_name == "ENERGY":
                                total_on_board = 0
                                if active_poke and len(active_poke) > 0:
                                    total_on_board += len(get_val(active_poke[0], "attached", []))
                                for b in get_val(my_state, "bench", []):
                                    if b and len(b) > 0:
                                        total_on_board += len(get_val(b[0], "attached", []))
                                if total_on_board >= 8:
                                    base_score -= 8.0  # Excess energy: more likely to discard
                                elif total_on_board >= 5:
                                    base_score -= 3.0
                            elif ct_name == "TRAINER":
                                if card_id_int in registry.learned_dos:
                                    base_score -= 6.0  # Reduce learned_dos bonus for discards
                            scored_options[i] = (idx, base_score)
            except Exception:
                pass
        
        # Sort options: lowest scoring first for discards, highest first otherwise
        if is_discard:
            scored_options.sort(key=lambda x: x[1])
        else:
            scored_options.sort(key=lambda x: x[1], reverse=True)

        selected = [idx for idx, _ in scored_options[:max_count]]
        
        # Ensure we return exactly max_count unique indices
        if len(selected) < max_count:
            for idx in range(len(options)):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
        return selected
    except Exception as e:
        import sys
        sys.stderr.write(f"[smart_choice] Exception during choice: {e}\n")
        return fallback_action


def make_smart_choice(select, observation, fallback_action):
    global _registry
    try:
        options = get_val(select, "options") or get_val(select, "option") or []
        if not options:
            return fallback_action
            
        max_count = get_val(select, "maxCount", 1)
        sel_type = get_val(select, "type")
        
        # Resolve skills_dir for CardRegistry
        try:
            if _registry is None:
                from cb_agents.card_registry import CardRegistry
                import os
                from pathlib import Path
                agent_dir = str(Path(__file__).parent.resolve()) if "__file__" in globals() and globals()["__file__"] else os.getcwd()
                skills_dir = os.path.join(agent_dir, "skills")
                _registry = CardRegistry(skills_dir=skills_dir)
            registry = _registry
        except Exception:
            registry = None

        if registry is None:
            return fallback_action

        # Detect if this is likely a hand discard choice (cost for trainer or energy discard)
        is_discard = False
        if sel_type in (1, 2, 4):
            try:
                if sel_type == 4 or str(get_val(select, "context", "")).lower() in ("discard", "energy_discard"):
                    is_discard = True
                else:
                    # Check if all options point to cards in our hand
                    current = get_val(observation, "current")
                    my_idx = get_val(current, "yourIndex", 0)
                    players = get_val(current, "players", [])
                    if len(players) > my_idx:
                        my_hand_ids = [get_val(c, "id") for c in get_val(players[my_idx], "hand", []) if c and get_val(c, "id") is not None]
                        
                        option_card_ids = []
                        for opt in options:
                            opt_id = get_val(opt, "id")
                            if opt_id is None:
                                # Resolve coordinate
                                area = get_val(opt, "area")
                                index = get_val(opt, "index")
                                p_idx = get_val(opt, "playerIndex", 0)
                                if p_idx == my_idx and area == 2: # Hand
                                    hand = get_val(players[my_idx], "hand", [])
                                    if len(hand) > index:
                                        opt_id = get_val(hand[index], "id")
                            if opt_id is not None:
                                option_card_ids.append(opt_id)
                        
                        if option_card_ids and all(oid in my_hand_ids for oid in option_card_ids):
                            is_discard = True
            except Exception:
                pass

        def resolve_instance(val):
            if isinstance(val, list):
                return val[0] if len(val) > 0 else None
            return val

        # Collect board Pokemon names for evolution synergy mapping
        board_pokemon_names = set()
        try:
            current = get_val(observation, "current")
            my_idx = get_val(current, "yourIndex", 0)
            players = get_val(current, "players", [])
            if len(players) > my_idx:
                my_state = players[my_idx]
                act = resolve_instance(get_val(my_state, "active"))
                if act:
                    act_name = get_val(act, "name") or get_val(get_val(act, "card"), "name")
                    if act_name: board_pokemon_names.add(str(act_name).lower())
                for b in get_val(my_state, "bench", []):
                    b_resolved = resolve_instance(b)
                    if b_resolved:
                        b_name = get_val(b_resolved, "name") or get_val(get_val(b_resolved, "card"), "name")
                        if b_name: board_pokemon_names.add(str(b_name).lower())
        except Exception:
            pass

        # Score each option
        scored_options = []
        for idx, opt in enumerate(options):
            card_id = get_val(opt, "id")
            card_name = get_val(opt, "name", "")
            
            # If coordinates are present instead of name/id, resolve them
            if card_id is None and not card_name:
                try:
                    area = get_val(opt, "area")
                    index = get_val(opt, "index")
                    p_idx = get_val(opt, "playerIndex", 0)
                    current = get_val(observation, "current")
                    players = get_val(current, "players", [])
                    if len(players) > p_idx:
                        p_state = players[p_idx]
                        if area == 2: # Hand
                            hand = get_val(p_state, "hand", [])
                            if len(hand) > index:
                                card_id = get_val(hand[index], "id")
                        elif area == 12: # Bench
                            bench = get_val(p_state, "bench", [])
                            if len(bench) > index:
                                bench_item = resolve_instance(bench[index])
                                if bench_item is not None:
                                    card_id = get_val(bench_item, "id")
                        elif area == 4: # Active
                            active = get_val(p_state, "active", [])
                            if len(active) > index:
                                active_item = resolve_instance(active[index])
                                if active_item is not None:
                                    card_id = get_val(active_item, "id")
                except Exception:
                    pass

            card = None
            if card_id is not None:
                card = registry.get_full_skill(card_id)
            if card is None and card_name:
                card = registry.get_full_skill(card_name)
                
            score = 0.0
            if card:
                score = getattr(card, "utility_score", 0.0)
                
                # 1. Boost based on learned rules from Kaggle champions
                card_id_int = getattr(card, "card_id", None)
                if card_id_int is not None:
                    dos_set = getattr(registry, "_learned_dos_set", None)
                    if dos_set is None and hasattr(registry, "learned_dos"):
                        dos_data = getattr(registry, "learned_dos", {})
                        if isinstance(dos_data, dict):
                            dos_list = dos_data.get("deck_dos", [])
                            dos_set = {int(x.get("card_id")) for x in dos_list if isinstance(x, dict) and "card_id" in x}
                        else:
                            dos_set = set()
                        setattr(registry, "_learned_dos_set", dos_set)
                    donts_set = getattr(registry, "_learned_donts_set", None)
                    if donts_set is None and hasattr(registry, "learned_donts"):
                        donts_data = getattr(registry, "learned_donts", {})
                        if isinstance(donts_data, dict):
                            donts_list = donts_data.get("deck_donts", [])
                            donts_set = {int(x.get("card_id")) for x in donts_list if isinstance(x, dict) and "card_id" in x}
                        else:
                            donts_set = set()
                        setattr(registry, "_learned_donts_set", donts_set)

                    if dos_set and int(card_id_int) in dos_set:
                        score += 12.0
                    if donts_set and int(card_id_int) in donts_set:
                        score -= 12.0
                
                # 2. Boost if evolution predecessor is on board
                predecessor = registry.get_evolution_predecessor(getattr(card, "card_name", ""))
                if predecessor and predecessor.lower() in board_pokemon_names:
                    score += 15.0

                # 3. Energy Requirement / Active priority boost
                if sel_type in (1, 4) or str(get_val(select, "context", "")).lower() in ("energy", "attach"):
                    try:
                        area = get_val(opt, "area")
                        index = get_val(opt, "index")
                        p_idx = get_val(opt, "playerIndex", 0)
                        current = get_val(observation, "current")
                        my_idx = get_val(current, "yourIndex", 0)
                        if p_idx == my_idx:
                            players = get_val(current, "players", [])
                            my_state = players[my_idx]
                            instance = None
                            if area == 4: # Active
                                instance = resolve_instance(get_val(my_state, "active"))
                            elif area in (5, 12): # Bench
                                bench = get_val(my_state, "bench", [])
                                if len(bench) > index:
                                    instance = resolve_instance(bench[index])
                            if instance:
                                attached = get_val(instance, "attached", [])
                                attached_count = len(attached) if isinstance(attached, list) else 0
                                required = getattr(card, "energy_cost", 0)
                                if attached_count < required:
                                    # Avoid attaching energy to low-HP or non-attacking support/setup Pokemon
                                    target_name = ""
                                    target_id = get_val(instance, "id")
                                    if target_id is not None and registry:
                                        target_card = registry.get_full_skill(target_id)
                                        if target_card:
                                            target_name = getattr(target_card, "card_name", "").lower()
                                    
                                    is_passive_support = any(s in target_name for s in {"dunsparce", "bidoof", "snom", "remoraid", "jirachi", "manaphy"})
                                    target_hp = get_val(instance, "hp", 100)
                                    target_max_hp = get_val(instance, "maxHp", 100)
                                    is_low_hp = target_hp <= 40 and target_max_hp <= 130
                                    
                                    if is_passive_support or is_low_hp:
                                        boost = -15.0
                                    else:
                                        boost = 10.0 * (required - attached_count)
                                        if area == 4:
                                            boost += 5.0
                                    score += boost
                    except Exception:
                        pass
                
                # 4. Support Pokemon early match boost
                try:
                    current = get_val(observation, "current")
                    turn = get_val(current, "turn", 1)
                    if turn <= 5:
                        support_names = {"bidoof", "bibarel", "snom", "frosmoth", "remoraid", "octillery", "dunsparce", "jirachi", "manaphy", "mew"}
                        card_name_lower = getattr(card, "card_name", "").lower()
                        if any(s in card_name_lower for s in support_names):
                            score += 15.0
                except Exception:
                    pass
                
                if sel_type == 3:
                    score += getattr(card, "ev_score", 0.0) + (getattr(card, "damage_output", 0) * 0.01)
            scored_options.append((idx, score))

        # Value Network One-Step Lookahead Rescoring
        orch = globals().get("orchestrator")
        value_net = getattr(getattr(orch, "mcts", None), "value_network", None) if orch else None
        if value_net:
            try:
                import sys
                current_obs = get_val(observation, "current")
                players_list = get_val(current_obs, "players", [])
                my_idx_val = get_val(current_obs, "yourIndex", 0)
                my_state_dict = players_list[my_idx_val] if len(players_list) > my_idx_val else {}
                choice_ctx = str(get_val(select, "context", "")).lower()
                for i in range(len(scored_options)):
                    idx, base_score = scored_options[i]
                    opt = options[idx]
                    cid = get_val(opt, "id")
                    hyp_state = my_state_dict.copy() if isinstance(my_state_dict, dict) else {}
                    if is_discard and cid is not None:
                        cid_str = str(cid)
                        if cid_str in hyp_state.get("my_hand", []):
                            hand_copy = list(hyp_state["my_hand"])
                            hand_copy.remove(cid_str)
                            hyp_state["my_hand"] = hand_copy
                    elif (choice_ctx in ("draw", "search", "take")) and cid is not None:
                        cid_str = str(cid)
                        hand_copy = list(hyp_state.get("my_hand", []))
                        hand_copy.append(cid_str)
                        hyp_state["my_hand"] = hand_copy
                    
                    val_score = value_net.evaluate(hyp_state)
                    scored_options[i] = (idx, base_score + 10.0 * val_score)
            except Exception as val_err:
                import sys
                sys.stderr.write(f"[smart_choice] Value net evaluation failed: {val_err}\n")

        # Context-aware rescoring for discards: learned_dos +12 dominates utility (0-0.86)
        # so trainers always outscore Pokemon — but Pokemon win the game. Fix the balance.
        if is_discard:
            try:
                current = get_val(observation, "current")
                my_idx = get_val(current, "yourIndex", 0)
                players = get_val(current, "players", [])
                my_state = players[my_idx] if len(players) > my_idx else {}
                bench_slots = len(get_val(my_state, "bench", []))
                active_poke = get_val(my_state, "active", None)
                has_active = bool(active_poke and len(active_poke) > 0 and active_poke[0])
                my_hand = get_val(my_state, "hand", [])
                hand_ids = [get_val(c, "id") for c in my_hand if c]
                for i in range(len(scored_options)):
                    idx, base_score = scored_options[i]
                    opt = options[idx]
                    cid = get_val(opt, "id")
                    if cid is None:
                        area = get_val(opt, "area")
                        index = get_val(opt, "index")
                        if area == 2 and len(my_hand) > index:
                            cid = get_val(my_hand[index], "id")
                    if cid is not None:
                        card = registry.get_full_skill(cid)
                        if card:
                            ct = getattr(card, "card_type", None)
                            ct_name = ct.name if ct else ""
                            card_id_int = int(cid) if not isinstance(cid, int) else cid
                            if ct_name == "POKEMON":
                                count_in_hand = sum(1 for hid in hand_ids if str(hid) == str(cid))
                                is_last_copy = count_in_hand <= 1
                                bench_needed = (6 - bench_slots) if has_active else (6 - bench_slots - 1)
                                if bench_needed > 0 and is_last_copy:
                                    base_score += 25.0  # Strong survival bonus for last Pokemon copy
                                elif bench_needed > 0:
                                    base_score += 10.0
                            elif ct_name == "ENERGY":
                                total_on_board = 0
                                if active_poke and len(active_poke) > 0:
                                    total_on_board += len(get_val(active_poke[0], "attached", []))
                                for b in get_val(my_state, "bench", []):
                                    if b and len(b) > 0:
                                        total_on_board += len(get_val(b[0], "attached", []))
                                if total_on_board >= 8:
                                    base_score -= 8.0  # Excess energy: more likely to discard
                                elif total_on_board >= 5:
                                    base_score -= 3.0
                            elif ct_name == "TRAINER":
                                if card_id_int in registry.learned_dos:
                                    base_score -= 6.0  # Reduce learned_dos bonus for discards
                            scored_options[i] = (idx, base_score)
            except Exception:
                pass
        
        # Sort options: lowest scoring first for discards, highest first otherwise
        if is_discard:
            scored_options.sort(key=lambda x: x[1])
        else:
            scored_options.sort(key=lambda x: x[1], reverse=True)

        selected = [idx for idx, _ in scored_options[:max_count]]
        
        # Ensure we return exactly max_count unique indices
        if len(selected) < max_count:
            for idx in range(len(options)):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
        return selected
    except Exception as e:
        import sys
        sys.stderr.write(f"[smart_choice] Exception during choice: {e}\n")
        return fallback_action


def make_smart_choice(select, observation, fallback_action):
    global _registry
    try:
        options = get_val(select, "option", [])
        if not options:
            return fallback_action
            
        max_count = get_val(select, "maxCount", 1)
        sel_type = get_val(select, "type")
        
        # Resolve skills_dir for CardRegistry
        try:
            if _registry is None:
                from cb_agents.card_registry import CardRegistry
                import os
                from pathlib import Path
                agent_dir = str(Path(__file__).parent.resolve()) if "__file__" in globals() and globals()["__file__"] else os.getcwd()
                skills_dir = os.path.join(agent_dir, "skills")
                _registry = CardRegistry(skills_dir=skills_dir)
            registry = _registry
        except Exception:
            registry = None

        if registry is None:
            return fallback_action

        # Detect if this is likely a hand discard choice (cost for trainer or energy discard)
        is_discard = False
        if sel_type in (1, 2, 4):
            try:
                if sel_type == 4 or str(get_val(select, "context", "")).lower() in ("discard", "energy_discard"):
                    is_discard = True
                else:
                    # Check if all options point to cards in our hand
                    current = get_val(observation, "current")
                    my_idx = get_val(current, "yourIndex", 0)
                    players = get_val(current, "players", [])
                    if len(players) > my_idx:
                        my_hand_ids = [get_val(c, "id") for c in get_val(players[my_idx], "hand", []) if c and get_val(c, "id") is not None]
                        
                        option_card_ids = []
                        for opt in options:
                            opt_id = get_val(opt, "id")
                            if opt_id is None:
                                # Resolve coordinate
                                area = get_val(opt, "area")
                                index = get_val(opt, "index")
                                p_idx = get_val(opt, "playerIndex", 0)
                                if p_idx == my_idx and area == 2: # Hand
                                    hand = get_val(players[my_idx], "hand", [])
                                    if len(hand) > index:
                                        opt_id = get_val(hand[index], "id")
                            if opt_id is not None:
                                option_card_ids.append(opt_id)
                        
                        if option_card_ids and all(oid in my_hand_ids for oid in option_card_ids):
                            is_discard = True
            except Exception:
                pass

        def resolve_instance(val):
            if isinstance(val, list):
                return val[0] if len(val) > 0 else None
            return val

        # Collect board Pokemon names for evolution synergy mapping
        board_pokemon_names = set()
        try:
            current = get_val(observation, "current")
            my_idx = get_val(current, "yourIndex", 0)
            players = get_val(current, "players", [])
            if len(players) > my_idx:
                my_state = players[my_idx]
                act = resolve_instance(get_val(my_state, "active"))
                if act:
                    act_name = get_val(act, "name") or get_val(get_val(act, "card"), "name")
                    if act_name: board_pokemon_names.add(str(act_name).lower())
                for b in get_val(my_state, "bench", []):
                    b_resolved = resolve_instance(b)
                    if b_resolved:
                        b_name = get_val(b_resolved, "name") or get_val(get_val(b_resolved, "card"), "name")
                        if b_name: board_pokemon_names.add(str(b_name).lower())
        except Exception:
            pass

        # Score each option
        scored_options = []
        for idx, opt in enumerate(options):
            card_id = get_val(opt, "id")
            card_name = get_val(opt, "name", "")
            
            # If coordinates are present instead of name/id, resolve them
            if card_id is None and not card_name:
                try:
                    area = get_val(opt, "area")
                    index = get_val(opt, "index")
                    p_idx = get_val(opt, "playerIndex", 0)
                    current = get_val(observation, "current")
                    players = get_val(current, "players", [])
                    if len(players) > p_idx:
                        p_state = players[p_idx]
                        if area == 2: # Hand
                            hand = get_val(p_state, "hand", [])
                            if len(hand) > index:
                                card_id = get_val(hand[index], "id")
                        elif area == 12: # Bench
                            bench = get_val(p_state, "bench", [])
                            if len(bench) > index:
                                bench_item = resolve_instance(bench[index])
                                if bench_item is not None:
                                    card_id = get_val(bench_item, "id")
                        elif area == 4: # Active
                            active = get_val(p_state, "active", [])
                            if len(active) > index:
                                active_item = resolve_instance(active[index])
                                if active_item is not None:
                                    card_id = get_val(active_item, "id")
                except Exception:
                    pass

            card = None
            if card_id is not None:
                card = registry.get_full_skill(card_id)
            if card is None and card_name:
                card = registry.get_full_skill(card_name)
                
            score = 0.0
            if card:
                score = getattr(card, "utility_score", 0.0)
                
                # 1. Boost based on learned rules from Kaggle champions
                card_id_int = getattr(card, "card_id", None)
                if card_id_int is not None:
                    if hasattr(registry, "learned_dos") and int(card_id_int) in registry.learned_dos:
                        score += 12.0
                    if hasattr(registry, "learned_donts") and int(card_id_int) in registry.learned_donts:
                        score -= 12.0
                
                # 2. Boost if evolution predecessor is on board
                predecessor = registry.get_evolution_predecessor(getattr(card, "card_name", ""))
                if predecessor and predecessor.lower() in board_pokemon_names:
                    score += 15.0

                # 3. Energy Requirement / Active priority boost
                if sel_type in (1, 4) or str(get_val(select, "context", "")).lower() in ("energy", "attach"):
                    try:
                        area = get_val(opt, "area")
                        index = get_val(opt, "index")
                        p_idx = get_val(opt, "playerIndex", 0)
                        current = get_val(observation, "current")
                        my_idx = get_val(current, "yourIndex", 0)
                        if p_idx == my_idx:
                            players = get_val(current, "players", [])
                            my_state = players[my_idx]
                            instance = None
                            if area == 4: # Active
                                instance = resolve_instance(get_val(my_state, "active"))
                            elif area == 12: # Bench
                                bench = get_val(my_state, "bench", [])
                                if len(bench) > index:
                                    instance = resolve_instance(bench[index])
                            if instance:
                                attached = get_val(instance, "attached", [])
                                attached_count = len(attached) if isinstance(attached, list) else 0
                                required = getattr(card, "energy_cost", 0)
                                if attached_count < required:
                                    # Avoid attaching energy to low-HP or non-attacking support/setup Pokemon
                                    target_name = ""
                                    target_id = get_val(instance, "id")
                                    if target_id is not None and registry:
                                        target_card = registry.get_full_skill(target_id)
                                        if target_card:
                                            target_name = getattr(target_card, "card_name", "").lower()
                                    
                                    is_passive_support = any(s in target_name for s in {"dunsparce", "bidoof", "snom", "remoraid", "jirachi", "manaphy"})
                                    target_hp = get_val(instance, "hp", 100)
                                    target_max_hp = get_val(instance, "maxHp", 100)
                                    is_low_hp = target_hp <= 40 and target_max_hp <= 130
                                    
                                    if is_passive_support or is_low_hp:
                                        boost = -15.0
                                    else:
                                        boost = 10.0 * (required - attached_count)
                                        if area == 4:
                                            boost += 5.0
                                    score += boost
                    except Exception:
                        pass
                
                # 4. Support Pokemon early match boost
                try:
                    current = get_val(observation, "current")
                    turn = get_val(current, "turn", 1)
                    if turn <= 5:
                        support_names = {"bidoof", "bibarel", "snom", "frosmoth", "remoraid", "octillery", "dunsparce", "jirachi", "manaphy", "mew"}
                        card_name_lower = getattr(card, "card_name", "").lower()
                        if any(s in card_name_lower for s in support_names):
                            score += 15.0
                except Exception:
                    pass
                
                if sel_type == 3:
                    score += getattr(card, "ev_score", 0.0) + (getattr(card, "damage_output", 0) * 0.01)

            scored_options.append((idx, score))

        # Context-aware rescoring for discards: learned_dos +12 dominates utility (0-0.86)
        # so trainers always outscore Pokemon — but Pokemon win the game. Fix the balance.
        if is_discard:
            try:
                current = get_val(observation, "current")
                my_idx = get_val(current, "yourIndex", 0)
                players = get_val(current, "players", [])
                my_state = players[my_idx] if len(players) > my_idx else {}
                bench_slots = len(get_val(my_state, "bench", []))
                active_poke = get_val(my_state, "active", None)
                has_active = bool(active_poke and len(active_poke) > 0 and active_poke[0])
                my_hand = get_val(my_state, "hand", [])
                hand_ids = [get_val(c, "id") for c in my_hand if c]
                for i in range(len(scored_options)):
                    idx, base_score = scored_options[i]
                    opt = options[idx]
                    cid = get_val(opt, "id")
                    if cid is None:
                        area = get_val(opt, "area")
                        index = get_val(opt, "index")
                        if area == 2 and len(my_hand) > index:
                            cid = get_val(my_hand[index], "id")
                    if cid is not None:
                        card = registry.get_full_skill(cid)
                        if card:
                            ct = getattr(card, "card_type", None)
                            ct_name = ct.name if ct else ""
                            card_id_int = int(cid) if not isinstance(cid, int) else cid
                            if ct_name == "POKEMON":
                                count_in_hand = sum(1 for hid in hand_ids if str(hid) == str(cid))
                                is_last_copy = count_in_hand <= 1
                                bench_needed = (6 - bench_slots) if has_active else (6 - bench_slots - 1)
                                if bench_needed > 0 and is_last_copy:
                                    base_score += 25.0  # Strong survival bonus for last Pokemon copy
                                elif bench_needed > 0:
                                    base_score += 10.0
                            elif ct_name == "ENERGY":
                                total_on_board = 0
                                if active_poke and len(active_poke) > 0:
                                    total_on_board += len(get_val(active_poke[0], "attached", []))
                                for b in get_val(my_state, "bench", []):
                                    if b and len(b) > 0:
                                        total_on_board += len(get_val(b[0], "attached", []))
                                if total_on_board >= 8:
                                    base_score -= 8.0  # Excess energy: more likely to discard
                                elif total_on_board >= 5:
                                    base_score -= 3.0
                            elif ct_name == "TRAINER":
                                if card_id_int in registry.learned_dos:
                                    base_score -= 6.0  # Reduce learned_dos bonus for discards
                            scored_options[i] = (idx, base_score)
            except Exception:
                pass
        
        # Sort options: lowest scoring first for discards, highest first otherwise
        if is_discard:
            scored_options.sort(key=lambda x: x[1])
        else:
            scored_options.sort(key=lambda x: x[1], reverse=True)

        selected = [idx for idx, _ in scored_options[:max_count]]
        
        # Ensure we return exactly max_count unique indices
        if len(selected) < max_count:
            for idx in range(len(options)):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
        return selected
    except Exception as e:
        import sys
        sys.stderr.write(f"[smart_choice] Exception during choice: {e}\n")
        return fallback_action


def make_smart_choice(select, observation, fallback_action):
    global _registry
    try:
        options = get_val(select, "option", [])
        if not options:
            return fallback_action
            
        max_count = get_val(select, "maxCount", 1)
        sel_type = get_val(select, "type")
        
        # Resolve skills_dir for CardRegistry
        try:
            if _registry is None:
                from cb_agents.card_registry import CardRegistry
                import os
                from pathlib import Path
                agent_dir = str(Path(__file__).parent.resolve()) if "__file__" in globals() and globals()["__file__"] else os.getcwd()
                skills_dir = os.path.join(agent_dir, "skills")
                _registry = CardRegistry(skills_dir=skills_dir)
            registry = _registry
        except Exception:
            registry = None

        if registry is None:
            return fallback_action

        # Detect if this is likely a hand discard choice (cost for trainer or energy discard)
        is_discard = False
        if sel_type in (1, 2, 4):
            try:
                if sel_type == 4 or str(get_val(select, "context", "")).lower() in ("discard", "energy_discard"):
                    is_discard = True
                else:
                    # Check if all options point to cards in our hand
                    current = get_val(observation, "current")
                    my_idx = get_val(current, "yourIndex", 0)
                    players = get_val(current, "players", [])
                    if len(players) > my_idx:
                        my_hand_ids = [get_val(c, "id") for c in get_val(players[my_idx], "hand", []) if c and get_val(c, "id") is not None]
                        
                        option_card_ids = []
                        for opt in options:
                            opt_id = get_val(opt, "id")
                            if opt_id is None:
                                # Resolve coordinate
                                area = get_val(opt, "area")
                                index = get_val(opt, "index")
                                p_idx = get_val(opt, "playerIndex", 0)
                                if p_idx == my_idx and area == 2: # Hand
                                    hand = get_val(players[my_idx], "hand", [])
                                    if len(hand) > index:
                                        opt_id = get_val(hand[index], "id")
                            if opt_id is not None:
                                option_card_ids.append(opt_id)
                        
                        if option_card_ids and all(oid in my_hand_ids for oid in option_card_ids):
                            is_discard = True
            except Exception:
                pass

        def resolve_instance(val):
            if isinstance(val, list):
                return val[0] if len(val) > 0 else None
            return val

        # Collect board Pokemon names for evolution synergy mapping
        board_pokemon_names = set()
        try:
            current = get_val(observation, "current")
            my_idx = get_val(current, "yourIndex", 0)
            players = get_val(current, "players", [])
            if len(players) > my_idx:
                my_state = players[my_idx]
                act = resolve_instance(get_val(my_state, "active"))
                if act:
                    act_name = get_val(act, "name") or get_val(get_val(act, "card"), "name")
                    if act_name: board_pokemon_names.add(str(act_name).lower())
                for b in get_val(my_state, "bench", []):
                    b_resolved = resolve_instance(b)
                    if b_resolved:
                        b_name = get_val(b_resolved, "name") or get_val(get_val(b_resolved, "card"), "name")
                        if b_name: board_pokemon_names.add(str(b_name).lower())
        except Exception:
            pass

        # Score each option
        scored_options = []
        for idx, opt in enumerate(options):
            card_id = get_val(opt, "id")
            card_name = get_val(opt, "name", "")
            
            # If coordinates are present instead of name/id, resolve them
            if card_id is None and not card_name:
                try:
                    area = get_val(opt, "area")
                    index = get_val(opt, "index")
                    p_idx = get_val(opt, "playerIndex", 0)
                    current = get_val(observation, "current")
                    players = get_val(current, "players", [])
                    if len(players) > p_idx:
                        p_state = players[p_idx]
                        if area == 2: # Hand
                            hand = get_val(p_state, "hand", [])
                            if len(hand) > index:
                                card_id = get_val(hand[index], "id")
                        elif area == 12: # Bench
                            bench = get_val(p_state, "bench", [])
                            if len(bench) > index:
                                bench_item = resolve_instance(bench[index])
                                if bench_item is not None:
                                    card_id = get_val(bench_item, "id")
                        elif area == 4: # Active
                            active = get_val(p_state, "active", [])
                            if len(active) > index:
                                active_item = resolve_instance(active[index])
                                if active_item is not None:
                                    card_id = get_val(active_item, "id")
                except Exception:
                    pass

            card = None
            if card_id is not None:
                card = registry.get_full_skill(card_id)
            if card is None and card_name:
                card = registry.get_full_skill(card_name)
                
            score = 0.0
            if card:
                score = getattr(card, "utility_score", 0.0)
                
                # 1. Boost based on learned rules from Kaggle champions
                card_id_int = getattr(card, "card_id", None)
                if card_id_int is not None:
                    if hasattr(registry, "learned_dos") and int(card_id_int) in registry.learned_dos:
                        score += 12.0
                    if hasattr(registry, "learned_donts") and int(card_id_int) in registry.learned_donts:
                        score -= 12.0
                
                # 2. Boost if evolution predecessor is on board
                predecessor = registry.get_evolution_predecessor(getattr(card, "card_name", ""))
                if predecessor and predecessor.lower() in board_pokemon_names:
                    score += 15.0

                # 3. Energy Requirement / Active priority boost
                if sel_type in (1, 4) or str(get_val(select, "context", "")).lower() in ("energy", "attach"):
                    try:
                        area = get_val(opt, "area")
                        index = get_val(opt, "index")
                        p_idx = get_val(opt, "playerIndex", 0)
                        current = get_val(observation, "current")
                        my_idx = get_val(current, "yourIndex", 0)
                        if p_idx == my_idx:
                            players = get_val(current, "players", [])
                            my_state = players[my_idx]
                            instance = None
                            if area == 4: # Active
                                instance = resolve_instance(get_val(my_state, "active"))
                            elif area == 12: # Bench
                                bench = get_val(my_state, "bench", [])
                                if len(bench) > index:
                                    instance = resolve_instance(bench[index])
                            if instance:
                                attached = get_val(instance, "attached", [])
                                attached_count = len(attached) if isinstance(attached, list) else 0
                                required = getattr(card, "energy_cost", 0)
                                if attached_count < required:
                                    # Avoid attaching energy to low-HP or non-attacking support/setup Pokemon
                                    target_name = ""
                                    target_id = get_val(instance, "id")
                                    if target_id is not None and registry:
                                        target_card = registry.get_full_skill(target_id)
                                        if target_card:
                                            target_name = getattr(target_card, "card_name", "").lower()
                                    
                                    is_passive_support = any(s in target_name for s in {"dunsparce", "bidoof", "snom", "remoraid", "jirachi", "manaphy"})
                                    target_hp = get_val(instance, "hp", 100)
                                    target_max_hp = get_val(instance, "maxHp", 100)
                                    is_low_hp = target_hp <= 40 and target_max_hp <= 130
                                    
                                    if is_passive_support or is_low_hp:
                                        boost = -15.0
                                    else:
                                        boost = 10.0 * (required - attached_count)
                                        if area == 4:
                                            boost += 5.0
                                    score += boost
                    except Exception:
                        pass
                
                # 4. Support Pokemon early match boost
                try:
                    current = get_val(observation, "current")
                    turn = get_val(current, "turn", 1)
                    if turn <= 5:
                        support_names = {"bidoof", "bibarel", "snom", "frosmoth", "remoraid", "octillery", "dunsparce", "jirachi", "manaphy", "mew"}
                        card_name_lower = getattr(card, "card_name", "").lower()
                        if any(s in card_name_lower for s in support_names):
                            score += 15.0
                except Exception:
                    pass
                
                if sel_type == 3:
                    score += getattr(card, "ev_score", 0.0) + (getattr(card, "damage_output", 0) * 0.01)

            scored_options.append((idx, score))

        # Context-aware rescoring for discards: learned_dos +12 dominates utility (0-0.86)
        # so trainers always outscore Pokemon — but Pokemon win the game. Fix the balance.
        if is_discard:
            try:
                current = get_val(observation, "current")
                my_idx = get_val(current, "yourIndex", 0)
                players = get_val(current, "players", [])
                my_state = players[my_idx] if len(players) > my_idx else {}
                bench_slots = len(get_val(my_state, "bench", []))
                active_poke = get_val(my_state, "active", None)
                has_active = bool(active_poke and len(active_poke) > 0 and active_poke[0])
                my_hand = get_val(my_state, "hand", [])
                hand_ids = [get_val(c, "id") for c in my_hand if c]
                for i in range(len(scored_options)):
                    idx, base_score = scored_options[i]
                    opt = options[idx]
                    cid = get_val(opt, "id")
                    if cid is None:
                        area = get_val(opt, "area")
                        index = get_val(opt, "index")
                        if area == 2 and len(my_hand) > index:
                            cid = get_val(my_hand[index], "id")
                    if cid is not None:
                        card = registry.get_full_skill(cid)
                        if card:
                            ct = getattr(card, "card_type", None)
                            ct_name = ct.name if ct else ""
                            card_id_int = int(cid) if not isinstance(cid, int) else cid
                            if ct_name == "POKEMON":
                                count_in_hand = sum(1 for hid in hand_ids if str(hid) == str(cid))
                                is_last_copy = count_in_hand <= 1
                                bench_needed = (6 - bench_slots) if has_active else (6 - bench_slots - 1)
                                if bench_needed > 0 and is_last_copy:
                                    base_score += 25.0  # Strong survival bonus for last Pokemon copy
                                elif bench_needed > 0:
                                    base_score += 10.0
                            elif ct_name == "ENERGY":
                                total_on_board = 0
                                if active_poke and len(active_poke) > 0:
                                    total_on_board += len(get_val(active_poke[0], "attached", []))
                                for b in get_val(my_state, "bench", []):
                                    if b and len(b) > 0:
                                        total_on_board += len(get_val(b[0], "attached", []))
                                if total_on_board >= 8:
                                    base_score -= 8.0  # Excess energy: more likely to discard
                                elif total_on_board >= 5:
                                    base_score -= 3.0
                            elif ct_name == "TRAINER":
                                if card_id_int in registry.learned_dos:
                                    base_score -= 6.0  # Reduce learned_dos bonus for discards
                            scored_options[i] = (idx, base_score)
            except Exception:
                pass
        
        # Sort options: lowest scoring first for discards, highest first otherwise
        if is_discard:
            scored_options.sort(key=lambda x: x[1])
        else:
            scored_options.sort(key=lambda x: x[1], reverse=True)

        selected = [idx for idx, _ in scored_options[:max_count]]
        
        # Ensure we return exactly max_count unique indices
        if len(selected) < max_count:
            for idx in range(len(options)):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
        return selected
    except Exception as e:
        import sys
        sys.stderr.write(f"[smart_choice] Exception during choice: {e}\n")
        return fallback_action


def make_smart_choice(select: dict, observation: dict, fallback_action: list[int], skills_dir: str) -> list[int]:
    global _registry
    try:
        options = select.get("options") or select.get("option") or []
        if not options:
            return fallback_action
            
        max_count = select.get("maxCount", 1)
        sel_type = select.get("type")
        
        # Load CardRegistry
        try:
            if _registry is None:
                from cb_agents.card_registry import CardRegistry
                _registry = CardRegistry(skills_dir=skills_dir)
            registry = _registry
        except Exception:
            registry = None

        if registry is None:
            return fallback_action

        # Detect if this is likely a hand discard choice (cost for trainer or energy discard)
        is_discard = False
        if sel_type in (1, 2, 4):
            try:
                if sel_type == 4 or str(select.get("context", "")).lower() in ("discard", "energy_discard"):
                    is_discard = True
                else:
                    # Check if all options point to cards in our hand
                    current = observation.get("current")
                    if current is not None:
                        my_idx = current.get("yourIndex", 0)
                        players = current.get("players", [])
                        if len(players) > my_idx and players[my_idx] is not None:
                            my_hand_ids = [c.get("id") for c in players[my_idx].get("hand", []) if c and c.get("id") is not None]
                            
                            option_card_ids = []
                            for opt in options:
                                opt_id = opt.get("id")
                                if opt_id is None:
                                    # Resolve coordinate
                                    area = opt.get("area")
                                    index = opt.get("index")
                                    p_idx = opt.get("playerIndex", 0)
                                    if p_idx == my_idx and area == 2: # Hand
                                        hand = players[my_idx].get("hand", [])
                                        if len(hand) > index:
                                            opt_id = hand[index].get("id")
                                if opt_id is not None:
                                    option_card_ids.append(opt_id)
                            
                            if option_card_ids and all(oid in my_hand_ids for oid in option_card_ids):
                                is_discard = True
            except Exception:
                pass

        def resolve_instance(val):
            if isinstance(val, list):
                return val[0] if len(val) > 0 else None
            return val

        # Collect board Pokemon names for evolution synergy mapping
        board_pokemon_names = set()
        try:
            current = observation.get("current")
            if current is not None:
                my_idx = current.get("yourIndex", 0)
                players = current.get("players", [])
                if len(players) > my_idx and players[my_idx] is not None:
                    my_state = players[my_idx]
                    act = resolve_instance(my_state.get("active"))
                    if act:
                        # Try to resolve act card name
                        act_name = act.get("name")
                        if not act_name and act.get("card"):
                            act_name = act.get("card").get("name")
                        if act_name: board_pokemon_names.add(str(act_name).lower())
                    for b in my_state.get("bench", []):
                        b_resolved = resolve_instance(b)
                        if b_resolved:
                            b_name = b_resolved.get("name")
                            if not b_name and b_resolved.get("card"):
                                b_name = b_resolved.get("card").get("name")
                            if b_name: board_pokemon_names.add(str(b_name).lower())
        except Exception:
            pass

        # Score each option
        scored_options = []
        for idx, opt in enumerate(options):
            card_id = opt.get("id")
            card_name = opt.get("name", "")
            
            # If coordinates are present instead of name/id, resolve them
            if card_id is None and not card_name:
                try:
                    area = opt.get("area")
                    index = opt.get("index")
                    p_idx = opt.get("playerIndex", 0)
                    current = observation.get("current")
                    if current is not None:
                        players = current.get("players", [])
                        if len(players) > p_idx and players[p_idx] is not None:
                            p_state = players[p_idx]
                            if area == 2: # Hand
                                hand = p_state.get("hand", [])
                                if len(hand) > index:
                                    card_id = hand[index].get("id")
                            elif area == 12: # Bench
                                bench = p_state.get("bench", [])
                                if len(bench) > index:
                                    bench_item = resolve_instance(bench[index])
                                    if bench_item is not None:
                                        card_id = bench_item.get("id")
                            elif area == 4: # Active
                                active = p_state.get("active", [])
                                if len(active) > index:
                                    active_item = resolve_instance(active[index])
                                    if active_item is not None:
                                        card_id = active_item.get("id")
                except Exception:
                    pass

            card = None
            if card_id is not None:
                card = registry.get_full_skill(card_id)
            if card is None and card_name:
                card = registry.get_full_skill(card_name)
                
            score = 0.0
            if card:
                score = getattr(card, "utility_score", 0.0)
                
                # 1. Boost based on learned rules from Kaggle champions
                card_id_int = getattr(card, "card_id", None)
                if card_id_int is not None:
                    if hasattr(registry, "learned_dos") and int(card_id_int) in registry.learned_dos:
                        score += 12.0
                    if hasattr(registry, "learned_donts") and int(card_id_int) in registry.learned_donts:
                        score -= 12.0
                
                # 2. Boost if evolution predecessor is on board
                predecessor = registry.get_evolution_predecessor(getattr(card, "card_name", ""))
                if predecessor and predecessor.lower() in board_pokemon_names:
                    score += 15.0

                # 3. Energy Requirement / Active priority boost
                if sel_type in (1, 4) or str(select.get("context", "")).lower() in ("energy", "attach"):
                    try:
                        area = opt.get("area")
                        index = opt.get("index")
                        p_idx = opt.get("playerIndex", 0)
                        current = observation.get("current")
                        if current is not None:
                            my_idx = current.get("yourIndex", 0)
                            if p_idx == my_idx:
                                players = current.get("players", [])
                                my_state = players[my_idx]
                                instance = None
                                if area == 4: # Active
                                    instance = resolve_instance(my_state.get("active"))
                                elif area == 12: # Bench
                                    bench = my_state.get("bench", [])
                                    if len(bench) > index:
                                        instance = resolve_instance(bench[index])
                                if instance:
                                    attached = instance.get("attached", [])
                                    attached_count = len(attached) if isinstance(attached, list) else 0
                                    required = getattr(card, "energy_cost", 0)
                                    if attached_count < required:
                                        # Avoid attaching energy to low-HP or non-attacking support/setup Pokemon
                                        target_name = ""
                                        target_id = instance.get("id") if isinstance(instance, dict) else getattr(instance, "id", None)
                                        if target_id is not None and registry:
                                            target_card = registry.get_full_skill(target_id)
                                            if target_card:
                                                target_name = getattr(target_card, "card_name", "").lower()
                                        
                                        is_passive_support = any(s in target_name for s in {"dunsparce", "bidoof", "snom", "remoraid", "jirachi", "manaphy"})
                                        target_hp = instance.get("hp", 100) if isinstance(instance, dict) else getattr(instance, "hp", 100)
                                        target_max_hp = instance.get("maxHp", 100) if isinstance(instance, dict) else getattr(instance, "maxHp", 100)
                                        is_low_hp = target_hp <= 40 and target_max_hp <= 130
                                        
                                        if is_passive_support or is_low_hp:
                                            boost = -15.0
                                        else:
                                            boost = 10.0 * (required - attached_count)
                                            if area == 4:
                                                boost += 5.0
                                        score += boost
                    except Exception:
                        pass
                
                # 4. Support Pokemon early match boost
                try:
                    current = observation.get("current")
                    if current is not None:
                        turn = current.get("turn", 1)
                        if turn <= 5:
                            support_names = {"bidoof", "bibarel", "snom", "frosmoth", "remoraid", "octillery", "dunsparce", "jirachi", "manaphy", "mew"}
                            card_name_lower = getattr(card, "card_name", "").lower()
                            if any(s in card_name_lower for s in support_names):
                                score += 15.0
                except Exception:
                    pass
                
                if sel_type == 3:
                    score += getattr(card, "ev_score", 0.0) + (getattr(card, "damage_output", 0) * 0.01)

            scored_options.append((idx, score))

        # Context-aware rescoring for discards: learned_dos +12 dominates utility (0-0.86)
        if is_discard:
            try:
                current = observation.get("current", {})
                my_idx = current.get("yourIndex", 0)
                players = current.get("players", [])
                my_state = players[my_idx] if len(players) > my_idx else {}
                bench_slots = len(my_state.get("bench", []))
                active_poke = my_state.get("active", None)
                has_active = bool(active_poke and len(active_poke) > 0 and active_poke[0])
                my_hand = my_state.get("hand", [])
                hand_ids = [c.get("id") for c in my_hand if c]
                for i in range(len(scored_options)):
                    idx, base_score = scored_options[i]
                    opt = options[idx]
                    cid = opt.get("id")
                    if cid is None:
                        area = opt.get("area")
                        index = opt.get("index")
                        if area == 2 and len(my_hand) > index:
                            cid = my_hand[index].get("id")
                    if cid is not None:
                        card = registry.get_full_skill(cid)
                        if card:
                            ct = getattr(card, "card_type", None)
                            ct_name = ct.name if ct else ""
                            card_id_int = int(cid) if not isinstance(cid, int) else cid
                            if ct_name == "POKEMON":
                                count_in_hand = sum(1 for hid in hand_ids if str(hid) == str(cid))
                                is_last_copy = count_in_hand <= 1
                                bench_needed = (6 - bench_slots) if has_active else (6 - bench_slots - 1)
                                if bench_needed > 0 and is_last_copy:
                                    base_score += 25.0
                                elif bench_needed > 0:
                                    base_score += 10.0
                            elif ct_name == "ENERGY":
                                total_on_board = 0
                                if active_poke and len(active_poke) > 0:
                                    total_on_board += len(active_poke[0].get("attached", []))
                                for b in my_state.get("bench", []):
                                    if b and len(b) > 0:
                                        total_on_board += len(b[0].get("attached", []))
                                if total_on_board >= 8:
                                    base_score -= 8.0
                                elif total_on_board >= 5:
                                    base_score -= 3.0
                            elif ct_name == "TRAINER":
                                if card_id_int in registry.learned_dos:
                                    base_score -= 6.0
                            scored_options[i] = (idx, base_score)
            except Exception:
                pass
        
        # Sort options: lowest scoring first for discards, highest first otherwise
        if is_discard:
            scored_options.sort(key=lambda x: x[1])
        else:
            scored_options.sort(key=lambda x: x[1], reverse=True)

        selected = [idx for idx, _ in scored_options[:max_count]]
        
        # Ensure we return exactly max_count unique indices
        if len(selected) < max_count:
            for idx in range(len(options)):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
        return selected
    except Exception as e:
        logger.error(f"[smart_choice] Exception during choice: {e}")
        return fallback_action

