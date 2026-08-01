
def maybe_add_run_to_cli(cli: click.Group) -> None:
    if "run" not in cli.commands:
        if state.file or state.module:
            obj = get_typer_from_state()
            if obj:
                obj._add_completion = False
                click_obj = typer.main.get_command(obj)
                click_obj.name = "run"
                if not click_obj.help:
                    click_obj.help = "Run the provided Typer app."
                cli.add_command(click_obj)

