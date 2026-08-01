
def rich_format_error(self: click.ClickException) -> None:
    """Print richly formatted click errors.

    Called by custom exception handler to print richly formatted click errors.
    Mimics original click.ClickException.echo() function but with rich formatting.
    """
    # Don't do anything when it's a NoArgsIsHelpError (without importing it, cf. #1278)
    if self.__class__.__name__ == "NoArgsIsHelpError":
        return

    console = _get_rich_console(stderr=True)
    ctx: click.Context | None = getattr(self, "ctx", None)
    if ctx is not None:
        console.print(ctx.get_usage())

    if ctx is not None and ctx.command.get_help_option(ctx) is not None:
        console.print(
            RICH_HELP.format(
                command_path=ctx.command_path, help_option=ctx.help_option_names[0]
            ),
            style=STYLE_ERRORS_SUGGESTION,
        )

    console.print(
        Panel(
            highlighter(self.format_message()),
            border_style=STYLE_ERRORS_PANEL_BORDER,
            title=ERRORS_PANEL_TITLE,
            title_align=ALIGN_ERRORS_PANEL,
        )
    )

