from . import _registry, logger

def _ss_ko_threat(v, gs, ac, mp):
    opp_damage = gs.get("_projected_opponent_damage", None)
    if opp_damage is None:
        try:
            opp_active = gs.get("opponent_active_pokemon", gs.get("opponent_active", {}))
            if isinstance(opp_active, dict) and opp_active.get("id"):
                from cb_agents.card_registry import CardRegistry
                reg = CardRegistry()
                oid = int(opp_active["id"]) if not isinstance(opp_active["id"], int) else opp_active["id"]
                ocard = reg.get_full_skill(oid)
                if ocard and ocard.damage_output:
                    opp_att = len(opp_active.get("attached", []) or opp_active.get("energies", []))
                    if opp_att >= max(1, ocard.energy_cost):
                        opp_damage = ocard.damage_output
                        atk_type = reg.card_poke_type.get(oid, "")
                        my_active = gs.get("my_active_pokemon", {})
                        if isinstance(my_active, dict) and my_active.get("id"):
                            my_id = int(my_active["id"]) if not isinstance(my_active["id"], int) else my_active["id"]
                            weak = reg.card_weakness.get(my_id, ""); resist = reg.card_resistance.get(my_id, "")
                            if atk_type and weak and atk_type == weak: opp_damage *= 2
                            if atk_type and resist and atk_type == resist: opp_damage = max(0, opp_damage - 30)
        except Exception: opp_damage = 0
    else:
        try: opp_damage = int(opp_damage)
        except (TypeError, ValueError): opp_damage = 0
    if opp_damage is None: opp_damage = 0
    my_hp = gs.get("my_active_hp") or 100
    if opp_damage > 0 and opp_damage >= my_hp:
        my_active_card_id = ac.get("id") if isinstance(ac, dict) else None
        is_one_prizer = True
        if my_active_card_id:
            try:
                card = _registry.get_full_skill(my_active_card_id)
                if card and any(t in card.card_name.lower() for t in (" ex", " v", "vstar", "vmax", "ex")):
                    is_one_prizer = False
            except Exception: pass
        has_iono = any("iono" in str(c).lower() for c in gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else False
        if is_one_prizer and has_iono and mp > 2: v += 0.2
        else: v -= 0.8
    elif opp_damage > 0 and opp_damage >= my_hp * 0.6: v -= 0.3
    return v
