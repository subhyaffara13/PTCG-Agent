
def normalize_action(raw_action: str, offset_play: int, offset_attack: int, offset_other: int) -> int:
    if not raw_action:
        return offset_other + 999  # Pass

    if raw_action.startswith("attack:"):
        return offset_attack + (_deterministic_hash(raw_action) % 1000)

    if raw_action.startswith("play_trainer:"):
        tn = raw_action.split(":", 1)[1]
        return offset_play + (_deterministic_hash(tn) % 1000)

    return offset_other + (_deterministic_hash(raw_action) % 1000)


def normalize_action(raw_action: str, offset_play: int, offset_attack: int, offset_other: int) -> int:
    """Maps action string to an integer action ID with deterministic structured encoding."""
    if not raw_action:
        return offset_other + 999  # Pass

    if raw_action.startswith("attack:"):
        return offset_attack + (_deterministic_hash(raw_action) % 1000)

    if raw_action.startswith("play_trainer:"):
        tn = raw_action.split(":", 1)[1]
        return offset_play + (_deterministic_hash(tn) % 1000)

    if raw_action.startswith("retreat:"):
        parts = raw_action.split(":")
        if len(parts) >= 2 and parts[1].lstrip("-").isdigit():
            return offset_play + (int(parts[1]) % 1000)
        return offset_play + (_deterministic_hash(raw_action) % 1000)

    if raw_action.startswith("play:") or raw_action.startswith("bench:") or raw_action.startswith("evolve:") or raw_action.startswith("attach_energy:") or raw_action.startswith("ability:"):
        parts = raw_action.split(":")
        if len(parts) >= 2 and parts[1].lstrip("-").isdigit():
            return offset_play + (int(parts[1]) % 1000)
        return offset_play + (_deterministic_hash(raw_action) % 1000)

    return offset_other + 1


def normalize_action(raw_action: str, offset_play: int, offset_attack: int, offset_other: int) -> int:
    if not raw_action:
        return offset_other + 999  # Pass

    if raw_action.startswith("attack:"):
        return offset_attack + (_deterministic_hash(raw_action) % 1000)

    if raw_action.startswith("play_trainer:"):
        tn = raw_action.split(":", 1)[1]
        return offset_play + (_deterministic_hash(tn) % 1000)

    return offset_other + (_deterministic_hash(raw_action) % 1000)

