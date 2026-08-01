
def get_command(typer_instance: Typer) -> click.Command:
    if typer_instance._add_completion:
        click_install_param, click_show_param = get_install_completion_arguments()
    if (
        typer_instance.registered_callback
        or typer_instance.info.callback
        or typer_instance.registered_groups
        or len(typer_instance.registered_commands) > 1
    ):
        # Create a Group
        click_command: click.Command = get_group(typer_instance)
        if typer_instance._add_completion:
            click_command.params.append(click_install_param)
            click_command.params.append(click_show_param)
        return click_command
    elif len(typer_instance.registered_commands) == 1:
        # Create a single Command
        single_command = typer_instance.registered_commands[0]

        if not single_command.context_settings and not isinstance(
            typer_instance.info.context_settings, DefaultPlaceholder
        ):
            single_command.context_settings = typer_instance.info.context_settings

        click_command = get_command_from_info(
            single_command,
            pretty_exceptions_short=typer_instance.pretty_exceptions_short,
            rich_markup_mode=typer_instance.rich_markup_mode,
        )
        if typer_instance._add_completion:
            click_command.params.append(click_install_param)
            click_command.params.append(click_show_param)
        return click_command
    raise RuntimeError(
        "Could not get a command for this Typer instance"
    )  # pragma: no cover

