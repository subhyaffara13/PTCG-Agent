from typing import Any

def shell_complete(
    cli: Command,
    ctx_args: cabc.MutableMapping[str, t.Any],
    prog_name: str,
    complete_var: str,
    instruction: str,
) -> t.Literal[0, 1]:
    """Perform shell completion for the given CLI program.

    :param cli: Command being called.
    :param ctx_args: Extra arguments to pass to
        ``cli.make_context``.
    :param prog_name: Name of the executable in the shell.
    :param complete_var: Name of the environment variable that holds
        the completion instruction.
    :param instruction: Value of ``complete_var`` with the completion
        instruction and shell, in the form ``instruction_shell``.
    :return: Status code to exit with.
    """
    shell, _, instruction = instruction.partition("_")
    comp_cls = get_completion_class(shell)

    if comp_cls is None:
        return 1

    comp = comp_cls(cli, ctx_args, prog_name, complete_var)

    # Write bytes, otherwise Windows text stdout translates LF to CRLF and breaks.
    if instruction == "source":
        echo(comp.source().encode(), nl=False)
        return 0

    if instruction == "complete":
        echo(comp.complete().encode())
        return 0

    return 1


def shell_complete(
    cli: click.Command,
    ctx_args: MutableMapping[str, Any],
    prog_name: str,
    complete_var: str,
    instruction: str,
) -> int:
    import click
    import click.shell_completion

    if "_" not in instruction:
        click.echo("Invalid completion instruction.", err=True)
        return 1

    # Click 8 changed the order/style of shell instructions from e.g.
    # source_bash to bash_source
    # Typer override to preserve the old style for compatibility
    # Original in Click 8.x commented:
    # shell, _, instruction = instruction.partition("_")
    instruction, _, shell = instruction.partition("_")
    # Typer override end

    comp_cls = click.shell_completion.get_completion_class(shell)

    if comp_cls is None:
        click.echo(f"Shell {shell} not supported.", err=True)
        return 1

    comp = comp_cls(cli, ctx_args, prog_name, complete_var)

    if instruction == "source":
        click.echo(comp.source())
        return 0

    # Typer override to print the completion help msg with Rich
    if instruction == "complete":
        click.echo(comp.complete())
        return 0
    # Typer override end

    click.echo(f'Completion instruction "{instruction}" not supported.', err=True)
    return 1

