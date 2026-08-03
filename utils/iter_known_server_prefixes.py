from typing import Any, Optional

def iter_known_server_prefixes(server: Any) -> Iterator[str]:
    """Yield every prefix form that may appear in tool names for ``server``.

    Always includes the *current* prefix returned by ``get_server_prefix``.
    Additionally yields the historical (alias / server_name / server_id) and
    short-ID forms so the routing layer can resolve tool names regardless of
    which prefix mode was active when the client first observed them.
    """
    seen = set()

    def _emit(value: Optional[str]) -> Iterator[str]:
        if value and value not in seen:
            seen.add(value)
            yield value

    yield from _emit(get_server_prefix(server))
    yield from _emit(getattr(server, "short_prefix", None))

    server_id = getattr(server, "server_id", None)
    if server_id:
        try:
            yield from _emit(compute_short_server_prefix(server_id))
        except ValueError:
            pass

    yield from _emit(getattr(server, "alias", None))
    yield from _emit(getattr(server, "server_name", None))
    yield from _emit(server_id)

