
def rich_format_help(
    *,
    obj: click.Command | click.Group,
    ctx: click.Context,
    markup_mode: MarkupModeStrict,
) -> None:
    """Print nicely formatted help text using rich.

    Based on original code from rich-cli, by @willmcgugan.
    https://github.com/Textualize/rich-cli/blob/8a2767c7a340715fc6fbf4930ace717b9b2fc5e5/src/rich_cli/__main__.py#L162-L236

    Replacement for the click function format_help().
    Takes a command or group and builds the help text output.
    """
    console = _get_rich_console()

    # Print usage
    console.print(
        Padding(highlighter(obj.get_usage(ctx)), 1), style=STYLE_USAGE_COMMAND
    )

    # Print command / group help if we have some
    if obj.help:
        # Print with some padding
        console.print(
            Padding(
                Align(
                    _get_help_text(
                        obj=obj,
                        markup_mode=markup_mode,
                    ),
                    pad=False,
                ),
                (0, 1, 1, 1),
            )
        )
    panel_to_arguments: defaultdict[str, list[click.Argument]] = defaultdict(list)
    panel_to_options: defaultdict[str, list[click.Option]] = defaultdict(list)
    for param in obj.get_params(ctx):
        # Skip if option is hidden
        if getattr(param, "hidden", False):
            continue
        if isinstance(param, click.Argument):
            panel_name = (
                getattr(param, _RICH_HELP_PANEL_NAME, None) or ARGUMENTS_PANEL_TITLE
            )
            panel_to_arguments[panel_name].append(param)
        elif isinstance(param, click.Option):
            panel_name = (
                getattr(param, _RICH_HELP_PANEL_NAME, None) or OPTIONS_PANEL_TITLE
            )
            panel_to_options[panel_name].append(param)
    default_arguments = panel_to_arguments.get(ARGUMENTS_PANEL_TITLE, [])
    _print_options_panel(
        name=ARGUMENTS_PANEL_TITLE,
        params=default_arguments,
        ctx=ctx,
        markup_mode=markup_mode,
        console=console,
    )
    for panel_name, arguments in panel_to_arguments.items():
        if panel_name == ARGUMENTS_PANEL_TITLE:
            # Already printed above
            continue
        _print_options_panel(
            name=panel_name,
            params=arguments,
            ctx=ctx,
            markup_mode=markup_mode,
            console=console,
        )
    default_options = panel_to_options.get(OPTIONS_PANEL_TITLE, [])
    _print_options_panel(
        name=OPTIONS_PANEL_TITLE,
        params=default_options,
        ctx=ctx,
        markup_mode=markup_mode,
        console=console,
    )
    for panel_name, options in panel_to_options.items():
        if panel_name == OPTIONS_PANEL_TITLE:
            # Already printed above
            continue
        _print_options_panel(
            name=panel_name,
            params=options,
            ctx=ctx,
            markup_mode=markup_mode,
            console=console,
        )

    if isinstance(obj, click.Group):
        panel_to_commands: defaultdict[str, list[click.Command]] = defaultdict(list)
        for command_name in obj.list_commands(ctx):
            command = obj.get_command(ctx, command_name)
            if command and not command.hidden:
                panel_name = (
                    getattr(command, _RICH_HELP_PANEL_NAME, None)
                    or COMMANDS_PANEL_TITLE
                )
                panel_to_commands[panel_name].append(command)

        # Identify the longest command name in all panels
        max_cmd_len = max(
            [
                len(command.name or "")
                for commands in panel_to_commands.values()
                for command in commands
            ],
            default=0,
        )

        # Print each command group panel
        default_commands = panel_to_commands.get(COMMANDS_PANEL_TITLE, [])
        _print_commands_panel(
            name=COMMANDS_PANEL_TITLE,
            commands=default_commands,
            markup_mode=markup_mode,
            console=console,
            cmd_len=max_cmd_len,
        )
        for panel_name, commands in panel_to_commands.items():
            if panel_name == COMMANDS_PANEL_TITLE:
                # Already printed above
                continue
            _print_commands_panel(
                name=panel_name,
                commands=commands,
                markup_mode=markup_mode,
                console=console,
                cmd_len=max_cmd_len,
            )

    # Epilogue if we have it
    if obj.epilog:
        # Remove single linebreaks, replace double with single
        lines = obj.epilog.split("\n\n")
        epilogue = "\n".join([x.replace("\n", " ").strip() for x in lines])
        epilogue_text = _make_rich_text(text=epilogue, markup_mode=markup_mode)
        console.print(Padding(Align(epilogue_text, pad=False), 1))

