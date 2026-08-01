
def _make_agent_command(binary: str, display_name: str) -> click.Command:
    @click.command(
        name=binary,
        context_settings={"ignore_unknown_options": True},
        short_help=f"Run {display_name} through your LiteLLM proxy",
    )
    @click.option("--skip-verify", is_flag=True, default=False, help=_SKIP_VERIFY_HELP)
    @click.argument("args", nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def _command(ctx: click.Context, skip_verify: bool, args: Sequence[str]) -> None:
        _launch(ctx, binary, list(args), skip_verify=skip_verify)

    _command.help = (
        f"Run {display_name} routed through your LiteLLM proxy.\n\n"
        f"Logs in with LiteLLM if needed, verifies your key against the proxy, "
        f"exports the env vars {binary} reads, then hands off. Any arguments are "
        f"forwarded to `{binary}`."
    )
    return _command

