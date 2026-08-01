
def score_action(action: str, gs: dict, threat: float = 0.0) -> float:
    key = (action, _gs_cache_key(gs), threat)
    cached = _score_action_cache.get(key)
    if cached is not None:
        return cached
    if _HAS_CPP_SCORE and _ptcg_core is not None:
        try:
            val = _ptcg_core.score_action(gs, action)
            _cache_score(key, val)
            return val
        except Exception as e:
            logger.debug(f"C++ score_action failed: {e}. Falling back to Python.")
    val = _score_action_python(action, gs, threat)
    _cache_score(key, val)
    return val


def score_action(action: str, gs: dict, threat: float = 0.0) -> float:
    v = 0.0
    dc = gs.get("my_deck_count", 60)
    mp = gs.get("my_prizes", 6)
    ahp = gs.get("my_active_hp", 100)
    bn = gs.get("my_bench", [])
    ac = gs.get("my_active_pokemon", {})
    opp_hp = gs.get("opponent_active_hp", 100)
    if action.startswith("attack:"):
        v += 1.2  # Attacks are almost always the best action
        if mp <= 1: v += 1.0  # Game-winning attack
        if mp <= 2: v += 0.3  # Close to winning
        opp_ac = gs.get("opponent_active_pokemon", {})
        if isinstance(ac, dict) and isinstance(opp_ac, dict):
            my_type = ac.get("element_type", "")
            opp_weak = opp_ac.get("weakness", "")
            if my_type and opp_weak and my_type.lower() == opp_weak.lower():
                v += 0.5  # Type advantage
        # Check if we can KO
        if isinstance(ac, dict):
            my_active_id = ac.get("id")
            if my_active_id is not None:
                try:
                    card = _registry.get_full_skill(my_active_id)
                    if card and card.damage_output >= opp_hp:
                        v += 1.5  # KO bonus — this is likely the winning move
                except:
                    pass
    elif action.startswith("evolve:"):
        v += 0.6
    elif action.startswith("attach_energy:"):
        v += 0.45  # Energy attachment is important for enabling attacks
        if isinstance(ac, dict):
            need = 2
            try:
                e = _registry.get_full_skill(ac.get("id"))
                if e and e.energy_cost > 0: need = e.energy_cost
            except: pass
            att = len(ac.get("attached", []))
            if att < need:
                v += 0.3  # Bonus for charging up active attacker
            elif att >= need:
                an = ac.get("card_name", "").lower()
                sc = any(sa in an for sa in {"raging bolt", "iron hands", "chien pao", "ceruledge", "garchomp", "roaring moon", "groudon", "kyogre"})
                nr = ahp <= 50 or gs.get("my_active_status", "") in {"poisoned", "burned", "asleep", "paralyzed"}
                if not sc and not nr: v -= 0.15
    elif action.startswith("bench:"):
        if not bn: v += 0.8
        else:
            bs = len(bn)
            if bs < 2: v += 0.4
            elif bs < 3: v += 0.25
            elif bs < 4: v += 0.15
            else: v += 0.05
            pr = gs.get("priority_profile", "aggro_push")
            tol = {"aggro_push": 0.15, "closing": 0.10, "disruption": -0.05, "setup": 0.15, "stall": -0.15}.get(pr, 0.0)
            if bs >= 4 and tol < 0: v += tol * bs * 0.3
            elif bs >= 5 and tol <= 0: v -= 0.4
    elif action.startswith("play_trainer:"):
        v += 0.4
        if dc <= 5:
            tn = action.split(":", 1)[1].lower()
            if any(k in tn for k in {"iono", "judge"}): v += 0.8
            elif any(k in tn for k in {"research", "professor"}): v -= 1.3
        if dc > 30:
            n = action.split(":", 1)[1].lower()
            sk = {"nest ball", "ultra ball", "quick ball", "level ball", "secret box", "mega signal", "team rocket's petrel"}
            if any(s in n for s in sk): v += min(0.25, dc * 0.005)
    elif action.startswith("ability:"):
        tn = action.split(":", 1)[1].lower()
        v += 0.35
        if dc <= 5 and any(d in tn for d in {"colress", "concealed"}): v -= 0.5
    elif action.startswith("retreat:"):
        v += 0.4 if ahp <= 60 else -0.2
        rsb = gs.get("retreat_score_boost", 0.0)
        if rsb > 0: v += rsb
    elif action == "pass":
        v -= 1.0  # Strongly discourage passing
    hs = len(gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else 0
    if hs >= 2 and dc > 10: v += 0.03 * min(hs, 5)
    return v


def score_action(action: str, gs: dict, threat: float = 0.0) -> float:
    key = (action, _gs_cache_key(gs), threat)
    cached = _score_action_cache.get(key)
    if cached is not None:
        return cached
    if _HAS_CPP_SCORE and _ptcg_core is not None:
        try:
            val = _ptcg_core.score_action(gs, action)
            _cache_score(key, val)
            return val
        except Exception as e:
            logger.debug(f"C++ score_action failed: {e}. Falling back to Python.")
    val = _score_action_python(action, gs, threat)
    _cache_score(key, val)
    return val

