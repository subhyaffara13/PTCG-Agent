from typing import List

def get_card_id(c):
    if hasattr(c, "id"): return getattr(c, "id")
    if isinstance(c, dict): return c.get("id") or c.get("cardId") or c.get("name")
    return None

def get_mapped_indices(action_label: str, options: list, game_state: dict = None) -> List[int]:
    """Resolves specific option indexes from action label by matching action types and names."""
    if action_label == "pass":
        return [i for i, opt in enumerate(options) if opt.get("type") == 14]
        
    target = action_label.split(":", 1)[1] if ":" in action_label else ""
    my_hand = game_state.get("my_hand", []) if game_state else []
    
    if action_label.startswith("target:"):
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

    # Try to map target (card ID) to an option using the hand index
    if action_label.startswith("attach_energy:") or action_label.startswith("bench:") or action_label.startswith("play_trainer:"):
        card_target = target.split(":")[0] if target else ""
        if card_target:
            target_str = str(card_target)
            for i, opt in enumerate(options):
                opt_type = opt.get("type")
                if opt_type in (7, 8):  # Play Card (includes energy/trainers) or Bench
                    hand_idx = opt.get("index", -1)
                    if 0 <= hand_idx < len(my_hand):
                        card_id = str(my_hand[hand_idx])
                        if card_id == target_str:
                            return [i]
    if target.isdigit():
        idx = int(target)
        if 0 <= idx < len(options) and not any(o.get("type") in (7,8) for o in options):
            return [idx]
            
    mapped_indices = []
    if action_label.startswith("attack:"):
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") in (12, 13)]
    elif action_label.startswith("attach_energy:"):
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 7]
    elif action_label.startswith("bench:") or action_label.startswith("evolve:"):
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 8]
    elif action_label.startswith("play_trainer:"):
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 7]
    elif action_label.startswith("retreat:"):
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") in (10, 12)]
        
    if not mapped_indices:
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 14]
        
    return mapped_indices
