
def select_candidate_group(candidates: list, groups: dict) -> list:
    MIN_CANDIDATES = 3
    from cb_agents.sequencing_engine import SequencingEngine
    for phase in SequencingEngine.PHASE_ORDER:
        phase_actions = groups.get(phase, [])
        if phase_actions:
            escape_actions = [a for a in candidates if a.startswith("attack:") or a == "pass"]
            merged = list(dict.fromkeys(phase_actions + escape_actions))
            if len(merged) >= MIN_CANDIDATES:
                return merged
    return candidates


def select_candidate_group(candidates: list, groups: dict) -> list:
    MIN_CANDIDATES = 3
    from cb_agents.sequencing_engine import SequencingEngine
    for phase in SequencingEngine.PHASE_ORDER:
        phase_actions = groups.get(phase, [])
        if phase_actions:
            escape_actions = [a for a in candidates if a.startswith("attack:") or a == "pass"]
            merged = list(dict.fromkeys(phase_actions + escape_actions))
            if len(merged) >= MIN_CANDIDATES:
                return merged
    return candidates

