
def get_backend(*, auto_select=True):
    """
    Return the name of the current backend.

    Parameters
    ----------
    auto_select : bool, default: True
        Whether to trigger backend resolution if no backend has been
        selected so far. If True, this ensures that a valid backend
        is returned. If False, this returns None if no backend has been
        selected so far.

        .. versionadded:: 3.10

        .. admonition:: Provisional

           The *auto_select* flag is provisional. It may be changed or removed
           without prior warning.

    See Also
    --------
    matplotlib.use
    """
    if auto_select:
        return rcParams['backend']
    else:
        backend = rcParams._get('backend')
        if backend is rcsetup._auto_backend_sentinel:
            return None
        else:
            return backend


def get_backend(group: ProcessGroup | None = None) -> Backend:
    """
    Return the backend of the given process group.

    Args:
        group (ProcessGroup, optional): The process group to work on. The
            default is the general main process group. If another specific group
            is specified, the calling process must be part of :attr:`group`.

    Returns:
        The backend of the given process group as a lower case string.

    """
    pg = group or _get_default_group()
    if _rank_not_in_group(pg):
        raise ValueError("Invalid process group specified")

    pg_store = _world.pg_map.get(pg, None)
    if pg_store is None:
        raise ValueError(
            f"Process group {pg} is not initialized in the world group map. Please initialize the group first."
        )

    return Backend(not_none(pg_store)[0])


def get_backend(device: _device) -> str | None:
    r"""
    Get the backend for symmetric memory allocation for a given device. If not
    found, return None.

    Args:
        device (`torch.device` or str): the device for which to get the backend.
    """
    return _SymmetricMemory.get_backend(torch.device(device))


def get_backend(
    platform: None | str | xla_client.Client = None
) -> xla_client.Client:
  return _get_backend_uncached(platform)

