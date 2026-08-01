
def HFCliCommand(topic: TOPIC_T, examples: list[str] | None = None) -> type[TyperCommand]:
    def format_epilog(self: click.Command, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        _format_epilog_no_indent(self.epilog, ctx, formatter)

    def format_options(self: TyperCommand, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        TyperCommand.format_options(self, ctx, formatter)
        # Skip the section for commands that define their own --format / --quiet / --json,
        # or for pass-through commands that forward args to an external binary.
        if _has_local_formatting_option(self):
            return
        if self.context_settings.get("ignore_unknown_options"):
            return
        _format_formatting_options_section(formatter)

    def parse_args(self: click.Command, ctx: click.Context, args: list[str]) -> list[str]:
        # Show help when a command with required arguments is invoked without any args
        # (mirrors group behavior: `hf jobs` prints help, so `hf download` should too).
        if not args and not ctx.resilient_parsing:
            if any(isinstance(p, click.Argument) and p.required for p in self.params):
                click.echo(ctx.get_help(), color=ctx.color)
                ctx.exit()
        return TyperCommand.parse_args(self, ctx, args)

    return type(
        f"TyperCommand{topic.capitalize()}",
        (TyperCommand,),
        {
            "context_class": StyledContext,
            "topic": topic,
            "examples": examples or [],
            "format_epilog": format_epilog,
            "format_options": format_options,
            "parse_args": parse_args,
        },
    )

