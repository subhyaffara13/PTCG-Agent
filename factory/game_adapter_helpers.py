from typing import List

def get_mapped_indices(action_label: str, options: list) -> List[int]:
    """Resolves specific option indexes from action label by matching action types and names."""
    mapped_indices = []
    target_name = action_label.split(":", 1)[1] if ":" in action_label else ""
    
    if action_label.startswith("attack:"):
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 13 and opt.get("name") == target_name]
        if not mapped_indices: mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 13]
    elif action_label.startswith("attach_energy:"):
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 9 and opt.get("name") == target_name]
        if not mapped_indices: mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 9]
    elif action_label.startswith("bench:") or action_label.startswith("evolve:"):
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 8 and opt.get("name") == target_name]
        if not mapped_indices: mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 8]
    elif action_label.startswith("play_trainer:"):
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 7 and opt.get("name") == target_name]
        if not mapped_indices: mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 7]
    elif action_label.startswith("retreat:"):
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 10 and opt.get("name") == target_name]
        if not mapped_indices: mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 10]
        
    if not mapped_indices or action_label == "pass":
        mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 14]
        
    return mapped_indices
