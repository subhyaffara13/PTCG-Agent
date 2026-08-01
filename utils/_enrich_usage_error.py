
def _enrich_usage_error(error: click.UsageError, label: str, items: list[tuple[str, str]]) -> None:
    """Append a list of available options or commands to a usage error message."""
    if not items or error.ctx is None or f"Available {label} for" in error.message:
        return
    cmd_path = error.ctx.command_path
    lines = [f"\n\nAvailable {label} for '{cmd_path}':"]
    for name, help_text in items:
        lines.append(f"  {name:30s} {help_text}")
    lines.append(f"\nRun '{cmd_path} --help' for full details.")
    if isinstance(error, click.NoSuchOption) and error.possibilities:
        lines.append(f"\nDid you mean: {', '.join(sorted(error.possibilities))}?")
        setattr(error, "possibilities", [])
    setattr(error, "message", error.message + "\n".join(lines))

