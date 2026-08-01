
def get_command_from_info(
    command_info: CommandInfo,
    *,
    pretty_exceptions_short: bool,
    rich_markup_mode: MarkupMode,
) -> click.Command:
    assert command_info.callback, "A command must have a callback function"
    name = command_info.name or get_command_name(command_info.callback.__name__)  # ty: ignore
    use_help = command_info.help
    if use_help is None:
        use_help = inspect.getdoc(command_info.callback)
    else:
        use_help = inspect.cleandoc(use_help)
    (
        params,
        convertors,
        context_param_name,
    ) = get_params_convertors_ctx_param_name_from_function(command_info.callback)
    cls = command_info.cls or TyperCommand
    command = cls(
        name=name,
        context_settings=command_info.context_settings,
        callback=get_callback(
            callback=command_info.callback,
            params=params,
            convertors=convertors,
            context_param_name=context_param_name,
            pretty_exceptions_short=pretty_exceptions_short,
        ),
        params=params,  # type: ignore
        help=use_help,
        epilog=command_info.epilog,
        short_help=command_info.short_help,
        options_metavar=command_info.options_metavar,
        add_help_option=command_info.add_help_option,
        no_args_is_help=command_info.no_args_is_help,
        hidden=command_info.hidden,
        deprecated=command_info.deprecated,
        rich_markup_mode=rich_markup_mode,
        # Rich settings
        rich_help_panel=command_info.rich_help_panel,
    )
    return command

