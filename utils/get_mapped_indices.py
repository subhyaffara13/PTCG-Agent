from typing import List, Any

def get_val(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)

def get_mapped_indices(action_label: str, options: list, game_state: dict | None = None) -> List[int]:
    """Resolves specific option indexes from action label by matching action types, target index strings, and names."""
    if not action_label:
        return []
    if action_label == "pass":
        return [i for i, opt in enumerate(options) if get_val(opt, "type") in (14, "End", "pass")]
        
    target = action_label.split(":", 1)[1] if ":" in action_label else ""
    my_hand = game_state.get("my_hand", []) if game_state else []
    
    if action_label.startswith("target:"):
        tgt_id = target
        tgt_slot = 0
        active = game_state.get("my_active_pokemon", {}) if game_state else {}
        if isinstance(active, dict) and str(active.get("id")) == tgt_id:
            tgt_slot = 0
        else:
            bench = game_state.get("my_bench", []) if game_state else []
            for idx, p in enumerate(bench):
                if isinstance(p, dict) and str(p.get("id")) == tgt_id:
                    tgt_slot = idx + 1
                    break
        
        for i, opt in enumerate(options):
            if get_val(opt, "slot") == tgt_slot or get_val(opt, "index") == tgt_slot:
                return [i]
        return [tgt_slot if tgt_slot < len(options) else 0]

    if action_label.startswith("attach_energy:") or action_label.startswith("bench:") or action_label.startswith("play_trainer:") or action_label.startswith("evolve:"):
        card_target = target.split(":")[0] if target else ""
        if card_target:
            target_str = card_target
            for i, opt in enumerate(options):
                opt_type = get_val(opt, "type")
                if opt_type in (7, 8, 9, "Play", "play", "Attach", "attach"):
                    hand_idx = get_val(opt, "index", -1)
                    if hand_idx is not None and isinstance(hand_idx, int) and 0 <= hand_idx < len(my_hand):
                        card_id = str(my_hand[hand_idx])
                        if card_id == target_str:
                            return [i]
            if card_target.isdigit():
                idx = int(card_target)
                if 0 <= idx < len(options):
                    return [idx]

    if action_label.startswith("take_prize:"):
        if target.isdigit():
            idx = int(target)
            if 0 <= idx < len(options):
                return [idx]
        return [0]

    if target.isdigit():
        idx = int(target)
        if 0 <= idx < len(options):
            return [idx]

    mapped_indices = []
    if action_label.startswith("attack:"):
        if target.isdigit():
            idx = int(target)
            if 0 <= idx < len(options):
                return [idx]
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (12, 13, "Attack", "attack")]
    elif action_label.startswith("attach_energy:"):
        parts = action_label.split(":")
        energy_name = parts[1] if len(parts) > 1 else ""
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (8, 9, "Attach", "attach", "Energy", "energy") and (not energy_name or str(get_val(opt, "name", "")).lower() == energy_name.lower())]
        if not mapped_indices:
            mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (8, 9, "Attach", "attach", "Energy", "energy")]
    elif action_label.startswith("bench:") or action_label.startswith("evolve:"):
        poke_name = action_label.split(":", 1)[1] if ":" in action_label else ""
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, 8, "Play", "play") and (not poke_name or str(get_val(opt, "name", "")).lower() == poke_name.lower())]
        if not mapped_indices:
            mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, 8, "Play", "play")]
    elif action_label.startswith("play_trainer:"):
        trainer_name = action_label.split(":", 1)[1] if ":" in action_label else ""
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play", "Trainer", "trainer") and (not trainer_name or str(get_val(opt, "name", "")).lower() == trainer_name.lower())]
        if not mapped_indices:
            mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play", "Trainer", "trainer")]
    elif action_label.startswith("retreat:"):
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (10, 12, "Retreat", "retreat")]
    elif action_label.startswith("ability:"):
        ability_name = action_label.split(":", 1)[1] if ":" in action_label else ""
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (9, 11, 15, "Ability", "ability") and (not ability_name or str(get_val(opt, "name", "")).lower() == ability_name.lower())]
        if not mapped_indices:
            mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (9, 11, 15, "Ability", "ability")]
            
    if not mapped_indices:
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (14, "End", "pass")]
    if not mapped_indices and options:
        mapped_indices = [0]
        
    return mapped_indices
