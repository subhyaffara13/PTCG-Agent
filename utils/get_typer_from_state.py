
def get_typer_from_state() -> typer.Typer | None:
    spec = None
    if state.file:
        module_name = state.file.name
        spec = importlib.util.spec_from_file_location(module_name, str(state.file))
    elif state.module:
        spec = importlib.util.find_spec(state.module)
    if spec is None:
        if state.file:
            typer.echo(f"Could not import as Python file: {state.file}", err=True)
        else:
            typer.echo(f"Could not import as Python module: {state.module}", err=True)
        sys.exit(1)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    obj = get_typer_from_module(module)
    return obj

