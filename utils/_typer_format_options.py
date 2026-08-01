
def _typer_format_options(
    self: click.core.Command, *, ctx: click.Context, formatter: click.HelpFormatter
) -> None:
    args = []
    opts = []
    for param in self.get_params(ctx):
        rv = param.get_help_record(ctx)
        if rv is not None:
            if param.param_type_name == "argument":
                args.append(rv)
            elif param.param_type_name == "option":
                opts.append(rv)

    if args:
        with formatter.section(_("Arguments")):
            formatter.write_dl(args)
    if opts:
        with formatter.section(_("Options")):
            formatter.write_dl(opts)

