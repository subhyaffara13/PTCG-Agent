
def _check_lethal_and_update(game_state: dict) -> None:
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    legal_attacks = game_state.get("legal_attacks", [])
    max_damage = 0
    if legal_attacks:
        for att in legal_attacks:
            dmg_val = 0
            if hasattr(registry, "move_damage") and att.lower() in registry.move_damage:
                try:
                    dmg_str = registry.move_damage[att.lower()].strip().lower()
                    if "x" in dmg_str or "×" in dmg_str or "?" in dmg_str:
                        dmg_val = 0
                    else:
                        if dmg_str.endswith("+"):
                            dmg_str = dmg_str[:-1]
                        dmg_str = "".join(c for c in dmg_str if c.isdigit())
                        dmg_val = int(dmg_str) if dmg_str else 0
                except Exception as e:
                    logger.debug(f"Parsing move_damage failed for {att}: {e}")
            else:
                my_active = game_state.get("my_active_pokemon")
                if my_active:
                    my_active_id = my_active.get("id") if isinstance(my_active, dict) else my_active
                    if my_active_id is not None:
                        try:
                            card = registry.get_full_skill(my_active_id)
                            if card:
                                dmg_val = card.damage_output
                        except Exception as e:
                            logger.debug(f"Registry get_full_skill lookup failed for {my_active_id}: {e}")
            max_damage = max(max_damage, dmg_val)

    lethal = pipeline.check_lethal(
        my_damage=max_damage,
        opp_hp=game_state.get("opponent_active_hp", 100),
        legal_attacks=legal_attacks,
        opp_active_id=game_state.get("opponent_active", {}).get("id") if isinstance(game_state.get("opponent_active"), dict) else game_state.get("opponent_active"),
        my_hp=game_state.get("my_active_hp", 100),
        legal_retreats=game_state.get("legal_retreats", []),
        my_attached=len(game_state.get("my_active_pokemon", {}).get("attached", [])) if isinstance(game_state.get("my_active_pokemon"), dict) else 0,
        boss_prob=game_state.get("boss_prob", 0.0),
    )
    if lethal.get("action_override"):
        game_state["lethal_action_override"] = lethal["action_override"]
    if lethal.get("retreat_score_boost"):
        game_state["retreat_score_boost"] = lethal["retreat_score_boost"]
        game_state["retreat_target"] = lethal.get("retreat_target")


def _check_lethal_and_update(game_state: dict) -> None:
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    legal_attacks = game_state.get("legal_attacks", [])
    max_damage = 0
    if legal_attacks:
        for att in legal_attacks:
            dmg_val = 0
            if hasattr(registry, "move_damage") and att.lower() in registry.move_damage:
                try:
                    dmg_str = registry.move_damage[att.lower()].strip().lower()
                    if "x" in dmg_str or "×" in dmg_str or "?" in dmg_str:
                        dmg_val = 0
                    else:
                        if dmg_str.endswith("+"):
                            dmg_str = dmg_str[:-1]
                        dmg_str = "".join(c for c in dmg_str if c.isdigit())
                        dmg_val = int(dmg_str) if dmg_str else 0
                except Exception as e:
                    logger.debug(f"Parsing move_damage failed for {att}: {e}")
            else:
                my_active = game_state.get("my_active_pokemon")
                if my_active:
                    my_active_id = my_active.get("id") if isinstance(my_active, dict) else my_active
                    if my_active_id is not None:
                        try:
                            card = registry.get_full_skill(my_active_id)
                            if card:
                                dmg_val = card.damage_output
                        except Exception as e:
                            logger.debug(f"Registry get_full_skill lookup failed for {my_active_id}: {e}")
            max_damage = max(max_damage, dmg_val)

    from cb_agents.heuristic_pipeline import pipeline
    lethal = pipeline.check_lethal(
        my_damage=max_damage,
        opp_hp=game_state.get("opponent_active_hp", 100),
        legal_attacks=legal_attacks,
        opp_active_id=game_state.get("opponent_active", {}).get("id") if isinstance(game_state.get("opponent_active"), dict) else game_state.get("opponent_active"),
        my_hp=game_state.get("my_active_hp", 100),
        legal_retreats=game_state.get("legal_retreats", []),
        my_attached=len(game_state.get("my_active_pokemon", {}).get("attached", [])) if isinstance(game_state.get("my_active_pokemon"), dict) else 0,
        boss_prob=game_state.get("boss_prob", 0.0),
    )
    if lethal.get("action_override"):
        game_state["lethal_action_override"] = lethal["action_override"]
    if lethal.get("retreat_score_boost"):
        game_state["retreat_score_boost"] = lethal["retreat_score_boost"]
        game_state["retreat_target"] = lethal.get("retreat_target")


def _check_lethal_and_update(game_state: dict) -> None:
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    legal_attacks = game_state.get("legal_attacks", [])
    max_damage = 0
    if legal_attacks:
        for att in legal_attacks:
            dmg_val = 0
            if hasattr(registry, "move_damage") and att.lower() in registry.move_damage:
                try:
                    dmg_str = registry.move_damage[att.lower()].strip().lower()
                    if "x" in dmg_str or "×" in dmg_str or "?" in dmg_str:
                        dmg_val = 0
                    else:
                        if dmg_str.endswith("+"):
                            dmg_str = dmg_str[:-1]
                        dmg_str = "".join(c for c in dmg_str if c.isdigit())
                        dmg_val = int(dmg_str) if dmg_str else 0
                except Exception as e:
                    logger.debug(f"Parsing move_damage failed for {att}: {e}")
            else:
                my_active = game_state.get("my_active_pokemon")
                if my_active:
                    my_active_id = my_active.get("id") if isinstance(my_active, dict) else my_active
                    if my_active_id is not None:
                        try:
                            card = registry.get_full_skill(my_active_id)
                            if card:
                                dmg_val = card.damage_output
                        except Exception as e:
                            logger.debug(f"Registry get_full_skill lookup failed for {my_active_id}: {e}")
            max_damage = max(max_damage, dmg_val)

    lethal = pipeline.check_lethal(
        my_damage=max_damage,
        opp_hp=game_state.get("opponent_active_hp", 100),
        legal_attacks=legal_attacks,
        opp_active_id=game_state.get("opponent_active", {}).get("id") if isinstance(game_state.get("opponent_active"), dict) else game_state.get("opponent_active"),
        my_hp=game_state.get("my_active_hp", 100),
        legal_retreats=game_state.get("legal_retreats", []),
        my_attached=len(game_state.get("my_active_pokemon", {}).get("attached", [])) if isinstance(game_state.get("my_active_pokemon"), dict) else 0,
        boss_prob=game_state.get("boss_prob", 0.0),
    )
    if lethal.get("action_override"):
        game_state["lethal_action_override"] = lethal["action_override"]
    if lethal.get("retreat_score_boost"):
        game_state["retreat_score_boost"] = lethal["retreat_score_boost"]
        game_state["retreat_target"] = lethal.get("retreat_target")


def _check_lethal_and_update(game_state: dict) -> None:
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    legal_attacks = game_state.get("legal_attacks", [])
    max_damage = 0
    if legal_attacks:
        for att in legal_attacks:
            dmg_val = 0
            if hasattr(registry, "move_damage") and att.lower() in registry.move_damage:
                try:
                    dmg_str = registry.move_damage[att.lower()].strip().lower()
                    if "x" in dmg_str or "×" in dmg_str or "?" in dmg_str:
                        dmg_val = 0
                    else:
                        if dmg_str.endswith("+"):
                            dmg_str = dmg_str[:-1]
                        dmg_str = "".join(c for c in dmg_str if c.isdigit())
                        dmg_val = int(dmg_str) if dmg_str else 0
                except Exception as e:
                    logger.debug(f"Parsing move_damage failed for {att}: {e}")
            else:
                my_active = game_state.get("my_active_pokemon")
                if my_active:
                    my_active_id = my_active.get("id") if isinstance(my_active, dict) else my_active
                    if my_active_id is not None:
                        try:
                            card = registry.get_full_skill(my_active_id)
                            if card:
                                dmg_val = card.damage_output
                        except Exception as e:
                            logger.debug(f"Registry get_full_skill lookup failed for {my_active_id}: {e}")
            max_damage = max(max_damage, dmg_val)

    from cb_agents.heuristic_pipeline import pipeline
    lethal = pipeline.check_lethal(
        my_damage=max_damage,
        opp_hp=game_state.get("opponent_active_hp", 100),
        legal_attacks=legal_attacks,
        opp_active_id=game_state.get("opponent_active", {}).get("id") if isinstance(game_state.get("opponent_active"), dict) else game_state.get("opponent_active"),
        my_hp=game_state.get("my_active_hp", 100),
        legal_retreats=game_state.get("legal_retreats", []),
        my_attached=len(game_state.get("my_active_pokemon", {}).get("attached", [])) if isinstance(game_state.get("my_active_pokemon"), dict) else 0,
        boss_prob=game_state.get("boss_prob", 0.0),
    )
    if lethal.get("action_override"):
        game_state["lethal_action_override"] = lethal["action_override"]
    if lethal.get("retreat_score_boost"):
        game_state["retreat_score_boost"] = lethal["retreat_score_boost"]
        game_state["retreat_target"] = lethal.get("retreat_target")


def _check_lethal_and_update(game_state: dict) -> None:
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    legal_attacks = game_state.get("legal_attacks", [])
    max_damage = 0
    if legal_attacks:
        for att in legal_attacks:
            dmg_val = 0
            if hasattr(registry, "move_damage") and att.lower() in registry.move_damage:
                try:
                    dmg_str = registry.move_damage[att.lower()].strip().lower()
                    if "x" in dmg_str or "×" in dmg_str or "?" in dmg_str:
                        dmg_val = 0
                    else:
                        if dmg_str.endswith("+"):
                            dmg_str = dmg_str[:-1]
                        dmg_str = "".join(c for c in dmg_str if c.isdigit())
                        dmg_val = int(dmg_str) if dmg_str else 0
                except:
                    pass
            else:
                my_active = game_state.get("my_active_pokemon")
                if my_active:
                    my_active_id = my_active.get("id") if isinstance(my_active, dict) else my_active
                    if my_active_id is not None:
                        try:
                            card = registry.get_full_skill(my_active_id)
                            if card:
                                dmg_val = card.damage_output
                        except:
                            pass
            max_damage = max(max_damage, dmg_val)

    lethal = pipeline.check_lethal(
        my_damage=max_damage,
        opp_hp=game_state.get("opponent_active_hp", 100),
        legal_attacks=legal_attacks,
        opp_active_id=game_state.get("opponent_active", {}).get("id") if isinstance(game_state.get("opponent_active"), dict) else game_state.get("opponent_active"),
        my_hp=game_state.get("my_active_hp", 100),
        legal_retreats=game_state.get("legal_retreats", []),
        my_attached=len(game_state.get("my_active_pokemon", {}).get("attached", [])) if isinstance(game_state.get("my_active_pokemon"), dict) else 0,
    )
    if lethal.get("action_override"):
        game_state["lethal_action_override"] = lethal["action_override"]
    if lethal.get("retreat_score_boost"):
        game_state["retreat_score_boost"] = lethal["retreat_score_boost"]
        game_state["retreat_target"] = lethal.get("retreat_target")

