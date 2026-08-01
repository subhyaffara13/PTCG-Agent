
def agent_profile(command: str) -> Tuple[str, FrozenSet[str]]:
    """Return the (display name, env profiles) for a wrapped command.

    Known agents map to the API family they speak. Anything else gets both
    families so it works regardless of which env vars the tool reads.
    """
    base = os.path.basename(command)
    if base in _KNOWN_AGENTS:
        return _KNOWN_AGENTS[base]
    return base, frozenset({PROFILE_ANTHROPIC, PROFILE_OPENAI})

