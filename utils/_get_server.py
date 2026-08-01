
def _get_server(
    environ: WSGIEnvironment,
) -> tuple[str, int | None] | None:
    name = environ.get("SERVER_NAME")

    if name is None:
        return None

    try:
        port: int | None = int(environ.get("SERVER_PORT", None))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        # unix socket
        port = None

    return name, port

