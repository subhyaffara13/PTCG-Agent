
def solve_typer_info_help(typer_info: TyperInfo) -> str:
    # Priority 1: Explicit value was set in app.add_typer()
    if not isinstance(typer_info.help, DefaultPlaceholder):
        return inspect.cleandoc(typer_info.help or "")
    # Priority 2: Explicit value was set in sub_app.callback()
    if typer_info.typer_instance and typer_info.typer_instance.registered_callback:
        callback_help = typer_info.typer_instance.registered_callback.help
        if not isinstance(callback_help, DefaultPlaceholder):
            return inspect.cleandoc(callback_help or "")
    # Priority 3: Explicit value was set in sub_app = typer.Typer()
    if typer_info.typer_instance and typer_info.typer_instance.info:
        instance_help = typer_info.typer_instance.info.help
        if not isinstance(instance_help, DefaultPlaceholder):
            return inspect.cleandoc(instance_help or "")
    # Priority 4: Implicit inference from callback docstring in app.add_typer()
    if typer_info.callback:
        doc = inspect.getdoc(typer_info.callback)
        if doc:
            return doc
    # Priority 5: Implicit inference from callback docstring in @app.callback()
    if typer_info.typer_instance and typer_info.typer_instance.registered_callback:
        callback = typer_info.typer_instance.registered_callback.callback
        if not isinstance(callback, DefaultPlaceholder):
            doc = inspect.getdoc(callback or "")
            if doc:
                return doc
    # Priority 6: Implicit inference from callback docstring in typer.Typer()
    if typer_info.typer_instance and typer_info.typer_instance.info:
        instance_callback = typer_info.typer_instance.info.callback
        if not isinstance(instance_callback, DefaultPlaceholder):
            doc = inspect.getdoc(instance_callback)
            if doc:
                return doc
    # Value not set, use the default
    return typer_info.help.value

