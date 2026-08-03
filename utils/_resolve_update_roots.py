from pathlib import Path


def _resolve_update_roots(
    *,
    claude: bool,
    global_: bool,
    dest: Path | None,
) -> list[Path]:
    if dest is not None:
        if claude or global_:
            raise CLIError("--dest cannot be combined with --claude or --global.")
        return [dest.expanduser().resolve()]

    roots: list[Path] = [CENTRAL_GLOBAL if global_ else CENTRAL_LOCAL]
    if claude:
        roots.append(CLAUDE_GLOBAL if global_ else CLAUDE_LOCAL)
    return [root.expanduser().resolve() for root in roots]

