
def _version_callback(value: bool) -> None:
    if value:
        print(__version__)
        raise typer.Exit()

