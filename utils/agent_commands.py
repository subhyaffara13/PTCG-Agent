
def agent_commands() -> List[click.Command]:
    """Build one top-level command per known agent, e.g. `lite claude`."""
    return [
        _make_agent_command(binary, name)
        for binary, (name, _profiles) in _KNOWN_AGENTS.items()
    ]

