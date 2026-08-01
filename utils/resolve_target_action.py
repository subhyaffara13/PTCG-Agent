
def resolve_target_action(target, options, game_state):
    tgt_id = target
    tgt_slot = 0
    active = game_state.get("my_active_pokemon", {})
    if isinstance(active, dict) and str(active.get("id")) == tgt_id:
        tgt_slot = 0
    else:
        bench = game_state.get("my_bench", [])
        for idx, p in enumerate(bench):
            if isinstance(p, dict) and str(p.get("id")) == tgt_id:
                tgt_slot = idx + 1
                break
    for i, opt in enumerate(options):
        if opt.get("slot") == tgt_slot or opt.get("index") == tgt_slot:
            return [i]
    return [tgt_slot if tgt_slot < len(options) else 0]

