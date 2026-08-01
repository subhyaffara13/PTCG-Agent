
def _get_parameter_help(
    *,
    param: click.Option | click.Argument | click.Parameter,
    ctx: click.Context,
    markup_mode: MarkupModeStrict,
) -> Columns:
    """Build primary help text for a click option or argument.

    Returns the prose help text for an option or argument, rendered either
    as a Rich Text object or as Markdown.
    Additional elements are appended to show the default and required status if
    applicable.
    """
    # import here to avoid cyclic imports
    from .core import TyperArgument, TyperOption

    items: list[Text | Markdown] = []

    # Get the environment variable first

    envvar = getattr(param, "envvar", None)
    var_str = ""
    # https://github.com/pallets/click/blob/0aec1168ac591e159baf6f61026d6ae322c53aaf/src/click/core.py#L2720-L2726
    if envvar is None:
        if (
            getattr(param, "allow_from_autoenv", None)
            and getattr(ctx, "auto_envvar_prefix", None) is not None
            and param.name is not None
        ):
            envvar = f"{ctx.auto_envvar_prefix}_{param.name.upper()}"
    if envvar is not None:
        var_str = (
            envvar if isinstance(envvar, str) else ", ".join(str(d) for d in envvar)
        )

    # Main help text
    help_value: str | None = getattr(param, "help", None)
    if help_value:
        paragraphs = help_value.split("\n\n")
        # Remove single linebreaks
        if markup_mode != MARKUP_MODE_MARKDOWN:
            paragraphs = [
                x.replace("\n", " ").strip()
                if not x.startswith("\b")
                else "{}\n".format(x.strip("\b\n"))
                for x in paragraphs
            ]
        items.append(
            _make_rich_text(
                text="\n".join(paragraphs).strip(),
                style=STYLE_OPTION_HELP,
                markup_mode=markup_mode,
            )
        )

    # Environment variable AFTER help text
    if envvar and getattr(param, "show_envvar", None):
        items.append(Text(ENVVAR_STRING.format(var_str), style=STYLE_OPTION_ENVVAR))

    # Default value
    # This uses Typer's specific param._get_default_string
    if isinstance(param, (TyperOption, TyperArgument)):
        default_value = param._extract_default_help_str(ctx=ctx)
        show_default_is_str = isinstance(param.show_default, str)
        if show_default_is_str or (
            default_value is not None and (param.show_default or ctx.show_default)
        ):
            default_str = param._get_default_string(
                ctx=ctx,
                show_default_is_str=show_default_is_str,
                default_value=default_value,
            )
            if default_str:
                items.append(
                    Text(
                        DEFAULT_STRING.format(default_str),
                        style=STYLE_OPTION_DEFAULT,
                    )
                )

    # Required?
    if param.required:
        items.append(Text(REQUIRED_LONG_STRING, style=STYLE_REQUIRED_LONG))

    # Use Columns - this allows us to group different renderable types
    # (Text, Markdown) onto a single line.
    return Columns(items)

