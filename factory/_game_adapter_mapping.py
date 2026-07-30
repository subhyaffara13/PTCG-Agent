from typing import List

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

def match_card_target(target_str, options, my_hand):
    for i, opt in enumerate(options):
        opt_type = opt.get("type")
        if opt_type in (7, 8, 9):
            hand_idx = opt.get("index", -1)
            if 0 <= hand_idx < len(my_hand) and str(my_hand[hand_idx]) == target_str:
                return [i]
    if target_str.isdigit():
        idx = int(target_str)
        if 0 <= idx < len(options):
            return [idx]
    return None

def resolve_action_type_mapping(action_label: str, options: list) -> List[int]:
    if action_label.startswith("attack:"):
        return [i for i, opt in enumerate(options) if opt.get("type") in (12, 13)]
    elif action_label.startswith("attach_energy:"):
        return [i for i, opt in enumerate(options) if opt.get("type") in (7, 9)]
    elif action_label.startswith("bench:") or action_label.startswith("evolve:"):
        return [i for i, opt in enumerate(options) if opt.get("type") == 8]
    elif action_label.startswith("play_trainer:"):
        return [i for i, opt in enumerate(options) if opt.get("type") == 7]
    elif action_label.startswith("retreat:"):
        return [i for i, opt in enumerate(options) if opt.get("type") in (10, 12)]
    elif action_label.startswith("ability:"):
        return [i for i, opt in enumerate(options) if opt.get("type") in (11, 15)]
    return []
