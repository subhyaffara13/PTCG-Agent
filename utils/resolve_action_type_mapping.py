from typing import List

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

