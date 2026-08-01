
def typer_factory(help: str, epilog: str | None = None, cls: type[TyperGroup] | None = None) -> "HFCliApp":
    """Create a Typer app with consistent settings.

    Args:
        help: Help text for the app.
        epilog: Optional epilog text (use `generate_epilog` to create one).
        cls: Optional Click group class to use (defaults to `HFCliTyperGroup`).

    Returns:
        A configured Typer app.
    """
    if cls is None:
        cls = HFCliTyperGroup
    return HFCliApp(
        help=help,
        epilog=epilog,
        add_completion=True,
        no_args_is_help=True,
        cls=cls,
        # Disable rich completely for consistent experience
        rich_markup_mode=None,
        rich_help_panel=None,
        pretty_exceptions_enable=False,
        # Disable TyperGroup's suggest_commands, it matches against raw aliased
        # keys ("list | ls") leaking pipe syntax into user-facing messages.
        # HFCliTyperGroup.resolve_command() handles suggestions with expanded names.
        suggest_commands=False,
        # Increase max content width for better readability
        context_settings={
            "max_content_width": 120,
            "help_option_names": ["-h", "--help"],
        },
    )

