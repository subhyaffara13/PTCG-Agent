from pathlib import Path


def skills_update(
    name: Annotated[
        str | None,
        typer.Argument(help="Optional installed skill name to update.", show_default=False),
    ] = None,
    claude: Annotated[bool, typer.Option("--claude", help="Update skills installed for Claude.")] = False,
    global_: Annotated[
        bool,
        typer.Option(
            "--global",
            "-g",
            help="Use global skills directories instead of the current project.",
        ),
    ] = False,
    dest: Annotated[
        Path | None,
        typer.Option(
            help="Update skills in a custom skills directory.",
        ),
    ] = None,
) -> None:
    """Update installed Hugging Face marketplace skills."""
    roots = _resolve_update_roots(claude=claude, global_=global_, dest=dest)

    results = _skills.update_skills(roots, selector=name)
    if not results:
        print("No installed skills found.")
        return

    for result in results:
        detail = f" ({result.detail})" if result.detail else ""
        print(f"{result.name}: {result.status}{detail}")

