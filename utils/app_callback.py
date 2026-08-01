
def app_callback(
    version: Annotated[
        bool | None, typer.Option("-v", "--version", callback=_version_callback, is_eager=True, hidden=True)
    ] = None,
) -> None:
    pass

