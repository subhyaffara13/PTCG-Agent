
def get_backend_config(group: ProcessGroup | None = None) -> str:
    """
    Return the backend configuration of the given process group.

    Args:
        group (ProcessGroup, optional): The process group to work on. The
            default is the general main process group. If another specific group
            is specified, the calling process must be part of :attr:`group`.

    Returns:
        The backend configuration of the given process group as a lower case string.

    """
    pg = group or _get_default_group()
    if _rank_not_in_group(pg):
        raise ValueError("Invalid process group specified")
    backend_config = _world.pg_backend_config.get(pg)
    return str(not_none(backend_config))

