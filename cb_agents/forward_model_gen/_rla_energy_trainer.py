from . import CardRegistry, logger

def _rla_add_energy_trainer_actions(gs, card, actions):
    if CardRegistry is None:
        return False
    c = None; ct = ""
    try:
        c = CardRegistry().get(int(card) if not isinstance(card, int) else card)
        if c: ct = getattr(c.card_type, "name", "")
    except Exception: pass
    if not c: return False
    if ct == "ENERGY":
        valid_targets = [str(gs.get("my_active_pokemon", {}).get("id", ""))] if isinstance(gs.get("my_active_pokemon"), dict) else []
        bench = gs.get("my_bench", [])
        if isinstance(bench, list):
            for p in bench:
                tid = str(p.get("id", "")) if isinstance(p, dict) else ""
                if tid: valid_targets.append(tid)
        if valid_targets:
            for target in valid_targets:
                if target: actions.append(f"attach_energy:{card}:{target}")
        else: actions.append(f"attach_energy:{card}")
        return True
    if ct == "TRAINER":
        skip = False
        if gs.get("supporter_played_this_turn"):
            try:
                fc = CardRegistry().get_full_skill(int(card) if not isinstance(card, int) else card)
                if fc and getattr(fc, 'trainer_subtype', None) and fc.trainer_subtype.name == "SUPPORTER":
                    skip = True
            except Exception: pass
        if not skip:
            actions.append(f"play_trainer:{c.card_name}")
        return True
    return False
