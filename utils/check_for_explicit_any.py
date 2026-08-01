
def check_for_explicit_any(
    typ: Type | None,
    options: Options,
    is_typeshed_stub: bool,
    msg: MessageBuilder,
    context: Context,
) -> None:
    if options.disallow_any_explicit and not is_typeshed_stub and typ and has_explicit_any(typ):
        msg.explicit_any(context)

