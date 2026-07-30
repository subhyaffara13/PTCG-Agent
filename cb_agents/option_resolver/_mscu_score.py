from .get_val_resolve_option_names import get_val

def _score_option_mscu(opt, registry, current, my_idx, sel_type, select):
    score = 0.0
    card_name = get_val(opt, "name", ""); card_id = get_val(opt, "id")
    card = None
    if card_id is not None: card = registry.get_full_skill(card_id)
    if card is None and card_name: card = registry.get_full_skill(card_name)
    if card:
        score = getattr(card, "utility_score", 0.0)
        card_id_int = getattr(card, "card_id", None)
        if card_id_int is not None and hasattr(registry, "learned_dos"):
            if int(card_id_int) in registry.learned_dos: score += 8.0
            if hasattr(registry, "learned_donts") and int(card_id_int) in registry.learned_donts: score -= 8.0
    try:
        players = get_val(current, "players", [])
        if len(players) > my_idx and players[my_idx]:
            bench = get_val(players[my_idx], "bench", []); bench_count = len(bench) if isinstance(bench, list) else 0
            opt_area = get_val(opt, "inPlayArea")
            if bench_count >= 4 and opt_area in (5, 12):
                cname_low = str(card_name).lower()
                is_tech_drop = any(t in cname_low for t in ("fezandipiti", "squawkabilly", "lumi", "rotom", "mew"))
                if not is_tech_drop: score -= 20.0
    except Exception: pass
    try:
        cname_low = str(card_name).lower()
        if "stadium" in cname_low or any(st in cname_low for st in ("court", "path", "temple", "beach", "chamber")):
            opp_stadium = get_val(current, "stadium", None)
            if not opp_stadium: score -= 10.0
            else: score += 15.0
    except Exception: pass
    try:
        players = get_val(current, "players", [])
        if len(players) > my_idx and players[my_idx]:
            cname_low = str(card_name).lower()
            is_draw_card = any(d in cname_low for d in ("research", "colress", "iono", "lillie", "draw", "pokégear", "trekking"))
            if is_draw_card:
                deck_count = len(get_val(players[my_idx], "deck", []))
                if deck_count <= 3: score -= 500.0
                elif deck_count <= 8: score -= 100.0
    except Exception: pass
    try:
        players = get_val(current, "players", [])
        if len(players) > my_idx and players[my_idx]:
            active_poke = get_val(players[my_idx], "active", {})
            status_list = get_val(active_poke, "specialConditions", []) or get_val(active_poke, "status", [])
            if status_list:
                cname_low = str(card_name).lower()
                is_cleanse = any(sw in cname_low for sw in ("switch", "rope", "cart", "scoop", "turo", "curler", "bird keeper"))
                if is_cleanse: score += 35.0
    except Exception: pass
    opt_type = get_val(opt, "type")
    if opt_type in (12, 13): score += 50.0
    elif opt_type == 8: score += 20.0
    return score

def _detect_discard_mscu(select, sel_type):
    if sel_type not in (1, 2, 4): return False
    if sel_type == 4 or str(get_val(select, "context", "")).lower() in ("discard", "energy_discard"): return True
    return False
