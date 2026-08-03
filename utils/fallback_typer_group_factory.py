from typing import Callable

def fallback_typer_group_factory(
    fallback_handler: FallbackHandlerT,
    extra_commands_provider: Callable[[], list[tuple[str, str]]] | None = None,
) -> type[HFCliTyperGroup]:
    """Return a Typer group class that runs a fallback handler before command resolution."""

    class FallbackTyperGroup(HFCliTyperGroup):
        def resolve_command(self, ctx: click.Context, args: list[str]) -> tuple:
            fallback_exit_code = fallback_handler(args, set(self.commands.keys()))
            if fallback_exit_code is not None:
                raise SystemExit(fallback_exit_code)
            return super().resolve_command(ctx, args)

        def format_commands(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
            super().format_commands(ctx, formatter)
            if extra_commands_provider is not None:
                entries = extra_commands_provider()
                if entries:
                    with formatter.section("Extension commands"):
                        formatter.write_dl(entries)

    return FallbackTyperGroup

