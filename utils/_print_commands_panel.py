from typing import Any

def _print_commands_panel(
    *,
    name: str,
    commands: list[click.Command],
    markup_mode: MarkupModeStrict,
    console: Console,
    cmd_len: int,
) -> None:
    t_styles: dict[str, Any] = {
        "show_lines": STYLE_COMMANDS_TABLE_SHOW_LINES,
        "leading": STYLE_COMMANDS_TABLE_LEADING,
        "box": STYLE_COMMANDS_TABLE_BOX,
        "border_style": STYLE_COMMANDS_TABLE_BORDER_STYLE,
        "row_styles": STYLE_COMMANDS_TABLE_ROW_STYLES,
        "pad_edge": STYLE_COMMANDS_TABLE_PAD_EDGE,
        "padding": STYLE_COMMANDS_TABLE_PADDING,
    }
    box_style = getattr(box, t_styles.pop("box"), None)

    commands_table = Table(
        highlight=False,
        show_header=False,
        expand=True,
        box=box_style,
        **t_styles,
    )
    # Define formatting in first column, as commands don't match highlighter
    # regex
    commands_table.add_column(
        style=STYLE_COMMANDS_TABLE_FIRST_COLUMN,
        no_wrap=True,
        width=cmd_len,
    )

    # A big ratio makes the description column be greedy and take all the space
    # available instead of allowing the command column to grow and misalign with
    # other panels.
    commands_table.add_column("Description", justify="left", no_wrap=False, ratio=10)
    rows: list[list[RenderableType | None]] = []
    deprecated_rows: list[RenderableType | None] = []
    for command in commands:
        helptext = command.short_help or command.help or ""
        command_name = command.name or ""
        if command.deprecated:
            command_name_text = Text(f"{command_name}", style=STYLE_DEPRECATED_COMMAND)
            deprecated_rows.append(Text(DEPRECATED_STRING, style=STYLE_DEPRECATED))
        else:
            command_name_text = Text(command_name)
            deprecated_rows.append(None)
        rows.append(
            [
                command_name_text,
                _make_command_help(
                    help_text=helptext,
                    markup_mode=markup_mode,
                ),
            ]
        )
    rows_with_deprecated = rows
    if any(deprecated_rows):
        rows_with_deprecated = []
        for row, deprecated_text in zip(rows, deprecated_rows, strict=True):
            rows_with_deprecated.append([*row, deprecated_text])
    for row in rows_with_deprecated:
        commands_table.add_row(*row)
    if commands_table.row_count:
        console.print(
            Panel(
                commands_table,
                border_style=STYLE_COMMANDS_PANEL_BORDER,
                title=name,
                title_align=ALIGN_COMMANDS_PANEL,
            )
        )

