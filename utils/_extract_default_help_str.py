
def _extract_default_help_str(
    obj: Union["TyperArgument", "TyperOption"], *, ctx: click.Context
) -> Any | Callable[[], Any] | None:
    # Extracted from click.core.Option.get_help_record() to be reused by
    # rich_utils avoiding RegEx hacks
    # Temporarily enable resilient parsing to avoid type casting
    # failing for the default. Might be possible to extend this to
    # help formatting in general.
    resilient = ctx.resilient_parsing
    ctx.resilient_parsing = True

    try:
        default_value = obj.get_default(ctx, call=False)
    finally:
        ctx.resilient_parsing = resilient
    return default_value

