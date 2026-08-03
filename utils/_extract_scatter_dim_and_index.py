from typing import Any

def _extract_scatter_dim_and_index(
    indices_arg: Any,
) -> tuple[int | None, fx.Node | None]:
    """Extract scatter dimension and index node from indices argument."""
    # Case 1: Single index → dim=0
    if not isinstance(indices_arg, (list, tuple)):
        return 0, indices_arg

    # List with Nones → position of non-None is dim
    index_node = None
    scatter_dim = None

    # Case 2 -> Find the first non-None index as the scatter dimension
    for dim, idx in enumerate(indices_arg):
        if idx is not None:
            if index_node is not None:
                # Multiple indices not supported
                return None, None
            index_node = idx
            scatter_dim = dim

    return scatter_dim, index_node

