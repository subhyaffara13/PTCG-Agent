from typing import Any

def _make_index_map(
    tiled_pairs: list[tuple[int, int]],
    buf_nd: int,
    n_grid: int,
) -> Any:
    """Return an index_map callable for ``pl.BlockSpec``.

    *tiled_pairs* is a list of ``(buf_axis, grid_dim)`` indicating which
    buffer axes receive a grid index.  All other axes return 0 (full block).

    All returned values are explicitly ``jnp.int32`` so that TPU Mosaic
    lowering (which rejects 64-bit types) works when ``jax_enable_x64`` is
    active.  The casts are created inside the function body (not captured)
    to satisfy JAX's "index_map must not capture constants" rule.
    """
    import jax.numpy as jnp  # pyrefly: ignore [import-error, missing-import]

    # Pre-build the mapping so the returned lambda is a plain lookup.
    mapping = dict(tiled_pairs)

    if n_grid == 0 or (n_grid == 1 and not mapping):
        return lambda _i: tuple(jnp.int32(0) for _ in range(buf_nd))

    def index_map(*grid_args):
        return tuple(
            jnp.int32(grid_args[mapping[d]]) if d in mapping else jnp.int32(0)
            for d in range(buf_nd)
        )

    return index_map

