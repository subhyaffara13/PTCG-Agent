
def resolve_option_names(options, observation, my_idx):
    global _registry
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

    if not registry:
        return

    try:
        current = get_val(observation, "current", {})
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return

        for opt in options:
            if not isinstance(opt, dict):
                continue
            card_id = get_val(opt, "id")
            if card_id is None:
                area = get_val(opt, "area")
                idx = get_val(opt, "index")
                p_idx = get_val(opt, "playerIndex", my_idx)
                target_player = players[p_idx] if 0 <= p_idx < len(players) else None
                if target_player and idx is not None:
                    if area == 2:  # Hand
                        hand = get_val(target_player, "hand", [])
                        if isinstance(hand, list) and 0 <= idx < len(hand):
                            card_item = hand[idx]
                            card_id = card_item.get("id") if isinstance(card_item, dict) else card_item
                    elif area == 4:  # Active
                        act_poke = get_val(target_player, "active")
                        if isinstance(act_poke, list) and act_poke: act_poke = act_poke[0]
                        if isinstance(act_poke, dict):
                            card_id = act_poke.get("id") or act_poke.get("card_id")
                    elif area in (5, 12):  # Bench
                        bench = get_val(target_player, "bench", [])
                        if isinstance(bench, list) and 0 <= idx < len(bench):
                            bench_item = bench[idx]
                            if isinstance(bench_item, dict):
                                card_id = bench_item.get("id") or bench_item.get("card_id")
                    elif area == 3:  # Discard
                        discard = get_val(target_player, "discard", [])
                        if isinstance(discard, list) and 0 <= idx < len(discard):
                            disc_item = discard[idx]
                            card_id = disc_item.get("id") if isinstance(disc_item, dict) else disc_item

            if card_id is not None:
                get_fn = getattr(registry, "get_full_skill", getattr(registry, "get", None))
                if get_fn:
                    card_entry = get_fn(card_id)
                    if card_entry and hasattr(card_entry, "card_name"):
                        opt["name"] = card_entry.card_name
                        opt["card_type"] = getattr(getattr(card_entry, "card_type", None), "name", "")
    except Exception as e:
        import sys
        sys.stderr.write(f"[resolve_option_names] Error: {e}\n")


def resolve_option_names(options, observation, my_idx):
    global _registry
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

    if not registry:
        return

    try:
        current = get_val(observation, "current", {})
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return

        for opt in options:
            if not isinstance(opt, dict):
                continue
            card_id = get_val(opt, "id")
            if card_id is None:
                area = get_val(opt, "area")
                idx = get_val(opt, "index")
                p_idx = get_val(opt, "playerIndex", my_idx)
                target_player = players[p_idx] if 0 <= p_idx < len(players) else None
                if target_player and idx is not None:
                    if area == 2:  # Hand
                        hand = get_val(target_player, "hand", [])
                        if isinstance(hand, list) and 0 <= idx < len(hand):
                            card_item = hand[idx]
                            card_id = card_item.get("id") if isinstance(card_item, dict) else card_item
                    elif area == 4:  # Active
                        act_poke = get_val(target_player, "active")
                        if isinstance(act_poke, list) and act_poke: act_poke = act_poke[0]
                        if isinstance(act_poke, dict):
                            card_id = act_poke.get("id") or act_poke.get("card_id")
                    elif area in (5, 12):  # Bench
                        bench = get_val(target_player, "bench", [])
                        if isinstance(bench, list) and 0 <= idx < len(bench):
                            bench_item = bench[idx]
                            if isinstance(bench_item, dict):
                                card_id = bench_item.get("id") or bench_item.get("card_id")
                    elif area == 3:  # Discard
                        discard = get_val(target_player, "discard", [])
                        if isinstance(discard, list) and 0 <= idx < len(discard):
                            disc_item = discard[idx]
                            card_id = disc_item.get("id") if isinstance(disc_item, dict) else disc_item

            if card_id is not None:
                get_fn = getattr(registry, "get_full_skill", getattr(registry, "get", None))
                if get_fn:
                    card_entry = get_fn(card_id)
                    if card_entry and hasattr(card_entry, "card_name"):
                        opt["name"] = card_entry.card_name
                        opt["card_type"] = getattr(getattr(card_entry, "card_type", None), "name", "")
    except Exception as e:
        import sys
        sys.stderr.write(f"[resolve_option_names] Error: {e}\n")


def resolve_option_names(options: list, observation: dict, my_idx: int, registry) -> None:
    """Dynamically resolves card names into option dictionaries based on hand/bench/active indices."""
    if not registry or not observation:
        return

    try:
        current = get_val(observation, "current", {})
        players = get_val(current, "players", [])
        if len(players) <= my_idx or not players[my_idx]:
            return

        my_state = players[my_idx]
        hand = get_val(my_state, "hand", [])

        for opt in options:
            if not isinstance(opt, dict):
                continue
            
            opt_type = opt.get("type")
            card_id = opt.get("id")
            
            # If coordinates are present (area=2 is hand, 4 is active, 5/12 is bench)
            if card_id is None:
                area = opt.get("area")
                idx = opt.get("index")
                p_idx = opt.get("playerIndex", my_idx)
                
                target_player = players[p_idx] if 0 <= p_idx < len(players) else None
                if target_player and idx is not None:
                    if area == 2:  # Hand
                        hand = get_val(target_player, "hand", [])
                        if isinstance(hand, list) and 0 <= idx < len(hand):
                            card_item = hand[idx]
                            card_id = card_item.get("id") if isinstance(card_item, dict) else card_item
                    elif area == 4:  # Active
                        act_poke = get_val(target_player, "active")
                        if isinstance(act_poke, list) and act_poke: act_poke = act_poke[0]
                        if isinstance(act_poke, dict):
                            card_id = act_poke.get("id") or act_poke.get("card_id")
                    elif area in (5, 12):  # Bench
                        bench = get_val(target_player, "bench", [])
                        if isinstance(bench, list) and 0 <= idx < len(bench):
                            bench_item = bench[idx]
                            if isinstance(bench_item, dict):
                                card_id = bench_item.get("id") or bench_item.get("card_id")
                    elif area == 3:  # Discard
                        discard = get_val(target_player, "discard", [])
                        if isinstance(discard, list) and 0 <= idx < len(discard):
                            disc_item = discard[idx]
                            card_id = disc_item.get("id") if isinstance(disc_item, dict) else disc_item

            if card_id is not None:
                opt["id"] = card_id
                card_entry = registry.get_full_skill(card_id)
                if card_entry and hasattr(card_entry, "card_name"):
                    opt["name"] = card_entry.card_name
                    opt["card_type"] = getattr(getattr(card_entry, "card_type", None), "name", "")
    except Exception:
        pass


def resolve_option_names(options, observation, my_idx):
    global _registry
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

    if not registry:
        return

    try:
        current = get_val(observation, "current", {})
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return

        my_state = players[my_idx]
        hand = get_val(my_state, "hand", [])

        for opt in options:
            opt_type = get_val(opt, "type")
            if opt_type in (7, 8, 9):
                area = get_val(opt, "area", 2)
                index = get_val(opt, "index")
                if area == 2 and index is not None and len(hand) > index:
                    card = hand[index]
                    card_id = get_val(card, "id")
                    if card_id is not None:
                        card_entry = registry.get(card_id)
                        if card_entry:
                            if isinstance(opt, dict):
                                opt["name"] = card_entry.card_name
                            else:
                                try:
                                    setattr(opt, "name", card_entry.card_name)
                                except:
                                    pass
    except Exception as e:
        import sys
        sys.stderr.write(f"[resolve_option_names] Error: {e}\n")


def resolve_option_names(options, observation, my_idx):
    global _registry
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

    if not registry:
        return

    try:
        current = get_val(observation, "current", {})
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return

        my_state = players[my_idx]
        hand = get_val(my_state, "hand", [])

        for opt in options:
            opt_type = get_val(opt, "type")
            if opt_type in (7, 8, 9):
                area = get_val(opt, "area", 2)
                index = get_val(opt, "index")
                if area == 2 and index is not None and len(hand) > index:
                    card = hand[index]
                    card_id = get_val(card, "id")
                    if card_id is not None:
                        card_entry = registry.get(card_id)
                        if card_entry:
                            if isinstance(opt, dict):
                                opt["name"] = card_entry.card_name
                            else:
                                try:
                                    setattr(opt, "name", card_entry.card_name)
                                except:
                                    pass
    except Exception as e:
        import sys
        sys.stderr.write(f"[resolve_option_names] Error: {e}\n")


def resolve_option_names(options: list, observation: dict, my_idx: int, registry) -> None:
    """Dynamically resolves card names into option dictionaries based on hand/bench/active indices."""
    if not registry or not observation:
        return

    try:
        current = get_val(observation, "current", {})
        players = get_val(current, "players", [])
        if len(players) <= my_idx or not players[my_idx]:
            return

        my_state = players[my_idx]
        hand = get_val(my_state, "hand", [])

        for opt in options:
            if not isinstance(opt, dict):
                continue
            
            opt_type = opt.get("type")
            card_id = opt.get("id")
            
            # If coordinates are present (area=2 is hand, 4 is active, 5/12 is bench)
            if card_id is None:
                area = opt.get("area")
                idx = opt.get("index")
                p_idx = opt.get("playerIndex", my_idx)
                
                target_player = players[p_idx] if 0 <= p_idx < len(players) else None
                if target_player and idx is not None:
                    if area == 2:  # Hand
                        hand = get_val(target_player, "hand", [])
                        if isinstance(hand, list) and 0 <= idx < len(hand):
                            card_item = hand[idx]
                            card_id = card_item.get("id") if isinstance(card_item, dict) else card_item
                    elif area == 4:  # Active
                        act_poke = get_val(target_player, "active")
                        if isinstance(act_poke, list) and act_poke: act_poke = act_poke[0]
                        if isinstance(act_poke, dict):
                            card_id = act_poke.get("id") or act_poke.get("card_id")
                    elif area in (5, 12):  # Bench
                        bench = get_val(target_player, "bench", [])
                        if isinstance(bench, list) and 0 <= idx < len(bench):
                            bench_item = bench[idx]
                            if isinstance(bench_item, dict):
                                card_id = bench_item.get("id") or bench_item.get("card_id")
                    elif area == 3:  # Discard
                        discard = get_val(target_player, "discard", [])
                        if isinstance(discard, list) and 0 <= idx < len(discard):
                            disc_item = discard[idx]
                            card_id = disc_item.get("id") if isinstance(disc_item, dict) else disc_item

            if card_id is not None:
                opt["id"] = card_id
                card_entry = registry.get_full_skill(card_id)
                if card_entry and hasattr(card_entry, "card_name"):
                    opt["name"] = card_entry.card_name
                    opt["card_type"] = getattr(getattr(card_entry, "card_type", None), "name", "")
    except Exception:
        pass

