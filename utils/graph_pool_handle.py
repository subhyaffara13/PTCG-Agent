
def graph_pool_handle() -> _POOL_HANDLE:
    r"""Return an opaque token representing the id of a graph memory pool.

    See :ref:`Graph memory management<graph-memory-management>`.

    .. warning::
        This API is in beta and may change in future releases.
    """
    return torch.cuda._POOL_HANDLE(_graph_pool_handle())


def graph_pool_handle() -> _POOL_HANDLE:
    """
    Return an opaque token representing the id of a graph memory pool.
    """
    # pyrefly: ignore [missing-attribute]
    return torch._C._mtia_graphPoolHandle()


def graph_pool_handle() -> _POOL_HANDLE:
    r"""Return an opaque token representing the id of a graph memory pool."""
    return torch.xpu._POOL_HANDLE(_xpu_graph_pool_handle())

