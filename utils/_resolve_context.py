
def _resolve_context(
    cli: Command,
    ctx_args: cabc.MutableMapping[str, t.Any],
    prog_name: str,
    args: list[str],
) -> Context:
    """Produce the context hierarchy starting with the command and
    traversing the complete arguments. This only follows the commands,
    it doesn't trigger input prompts or callbacks.

    :param cli: Command being called.
    :param prog_name: Name of the executable in the shell.
    :param args: List of complete args before the incomplete value.
    """
    ctx_args["resilient_parsing"] = True
    with cli.make_context(prog_name, args.copy(), **ctx_args) as ctx:
        args = ctx._protected_args + ctx.args

        while args:
            command = ctx.command

            if isinstance(command, Group):
                if not command.chain:
                    name, cmd, args = command.resolve_command(ctx, args)

                    if cmd is None:
                        return ctx

                    with cmd.make_context(
                        name, args, parent=ctx, resilient_parsing=True
                    ) as sub_ctx:
                        ctx = sub_ctx
                        args = ctx._protected_args + ctx.args
                else:
                    sub_ctx = ctx

                    while args:
                        name, cmd, args = command.resolve_command(ctx, args)

                        if cmd is None:
                            return ctx

                        with cmd.make_context(
                            name,
                            args,
                            parent=ctx,
                            allow_extra_args=True,
                            allow_interspersed_args=False,
                            resilient_parsing=True,
                        ) as sub_sub_ctx:
                            sub_ctx = sub_sub_ctx
                            args = sub_ctx.args

                    ctx = sub_ctx
                    args = [*sub_ctx._protected_args, *sub_ctx.args]
            else:
                break

    return ctx

