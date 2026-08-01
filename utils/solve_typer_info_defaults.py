
def solve_typer_info_defaults(typer_info: TyperInfo) -> TyperInfo:
    values: dict[str, Any] = {}
    for name, value in typer_info.__dict__.items():
        # Priority 1: Value was set in app.add_typer()
        if not isinstance(value, DefaultPlaceholder):
            values[name] = value
            continue
        # Priority 2: Value was set in @subapp.callback()
        try:
            callback_value = getattr(
                typer_info.typer_instance.registered_callback,  # type: ignore
                name,
            )
            if not isinstance(callback_value, DefaultPlaceholder):
                values[name] = callback_value
                continue
        except AttributeError:
            pass
        # Priority 3: Value set in subapp = typer.Typer()
        try:
            instance_value = getattr(
                typer_info.typer_instance.info,  # type: ignore
                name,
            )
            if not isinstance(instance_value, DefaultPlaceholder):
                values[name] = instance_value
                continue
        except AttributeError:
            pass
        # Value not set, use the default
        values[name] = value.value
    values["help"] = solve_typer_info_help(typer_info)
    return TyperInfo(**values)

