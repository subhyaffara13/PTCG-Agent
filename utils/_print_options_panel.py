
def _print_options_panel(
    *,
    name: str,
    params: list[click.Option] | list[click.Argument],
    ctx: click.Context,
    markup_mode: MarkupModeStrict,
    console: Console,
) -> None:
    options_rows: list[list[RenderableType]] = []
    required_rows: list[str | Text] = []
    for param in params:
        # Short and long form
        opt_long_strs = []
        opt_short_strs = []
        secondary_opt_long_strs = []
        secondary_opt_short_strs = []
        for opt_str in param.opts:
            if "--" in opt_str:
                opt_long_strs.append(opt_str)
            else:
                opt_short_strs.append(opt_str)
        for opt_str in param.secondary_opts:
            if "--" in opt_str:
                secondary_opt_long_strs.append(opt_str)
            else:
                secondary_opt_short_strs.append(opt_str)

        # Column for a metavar, if we have one
        metavar = Text(style=STYLE_METAVAR, overflow="fold")
        metavar_str = param.make_metavar(ctx=ctx)
        # Do it ourselves if this is a positional argument
        if (
            isinstance(param, click.Argument)
            and param.name
            and metavar_str == param.name.upper()
        ):
            metavar_str = param.type.name.upper()

        # Skip booleans and choices (handled above)
        if metavar_str != "BOOLEAN":
            metavar.append(metavar_str)

        # Range - from
        # https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2698-L2706  # noqa: E501
        # skip count with default range type
        if (
            isinstance(param.type, click.types._NumberRangeBase)
            and isinstance(param, click.Option)
            and not (param.count and param.type.min == 0 and param.type.max is None)
        ):
            range_str = param.type._describe_range()
            if range_str:
                metavar.append(RANGE_STRING.format(range_str))

        # Required asterisk
        required: str | Text = ""
        if param.required:
            required = Text(REQUIRED_SHORT_STRING, style=STYLE_REQUIRED_SHORT)

        required_rows.append(required)
        options_rows.append(
            [
                highlighter(",".join(opt_long_strs)),
                highlighter(",".join(opt_short_strs)),
                negative_highlighter(",".join(secondary_opt_long_strs)),
                negative_highlighter(",".join(secondary_opt_short_strs)),
                metavar_highlighter(metavar),
                _get_parameter_help(
                    param=param,
                    ctx=ctx,
                    markup_mode=markup_mode,
                ),
            ]
        )
    rows_with_required: list[list[RenderableType]] = []
    if any(required_rows):
        for required, row in zip(required_rows, options_rows, strict=True):
            rows_with_required.append([required, *row])
    else:
        rows_with_required = options_rows
    if options_rows:
        t_styles: dict[str, Any] = {
            "show_lines": STYLE_OPTIONS_TABLE_SHOW_LINES,
            "leading": STYLE_OPTIONS_TABLE_LEADING,
            "box": STYLE_OPTIONS_TABLE_BOX,
            "border_style": STYLE_OPTIONS_TABLE_BORDER_STYLE,
            "row_styles": STYLE_OPTIONS_TABLE_ROW_STYLES,
            "pad_edge": STYLE_OPTIONS_TABLE_PAD_EDGE,
            "padding": STYLE_OPTIONS_TABLE_PADDING,
        }
        box_style = getattr(box, t_styles.pop("box"), None)

        options_table = Table(
            highlight=True,
            show_header=False,
            expand=True,
            box=box_style,
            **t_styles,
        )
        for row in rows_with_required:
            options_table.add_row(*row)
        console.print(
            Panel(
                options_table,
                border_style=STYLE_OPTIONS_PANEL_BORDER,
                title=name,
                title_align=ALIGN_OPTIONS_PANEL,
            )
        )

