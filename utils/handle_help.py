
def handle_help(
    ctx: click.Context,
    param: click.Option | click.Parameter,
    value: typing.Any,
) -> None:
    if not value or ctx.resilient_parsing:
        return

    print_help()
    ctx.exit()

