
def skills_add(
    name: Annotated[
        str,
        typer.Argument(help="Marketplace skill name.", show_default=False),
    ] = DEFAULT_SKILL_ID,
    claude: Annotated[bool, typer.Option("--claude", help="Install for Claude.")] = False,
    global_: Annotated[
        bool,
        typer.Option(
            "--global",
            "-g",
            help="Install globally (user-level) instead of in the current project directory.",
        ),
    ] = False,
    dest: Annotated[
        Path | None,
        typer.Option(
            help="Install into a custom destination (path to skills directory).",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            help="Overwrite existing skills in the destination.",
        ),
    ] = False,
) -> None:
    """Download a Hugging Face skill and install it for an AI assistant.

    Default location is in the current directory (.agents/skills) or user-level (~/.agents/skills).
    If `--claude` is specified, the skill is also symlinked into Claude's legacy skills directory.
    """
    if dest is not None:
        if claude or global_:
            raise CLIError("--dest cannot be combined with --claude or --global.")
        skill_dest = _install_to(dest, name, force)
        print(f"Installed '{name}' to {skill_dest}")
        return

    # Install to central location
    central_path = CENTRAL_GLOBAL if global_ else CENTRAL_LOCAL
    central_skill_path = _install_to(central_path, name, force)
    print(f"Installed '{name}' to central location: {central_skill_path}")

    if claude:
        agent_target = CLAUDE_GLOBAL if global_ else CLAUDE_LOCAL
        link_path = _create_symlink(agent_target, name, central_skill_path, force)
        print(f"Created symlink: {link_path}")

