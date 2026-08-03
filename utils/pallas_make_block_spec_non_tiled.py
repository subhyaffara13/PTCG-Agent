from typing import Any

def pallas_make_block_spec_non_tiled(shape: tuple[int, ...]) -> Any:
    import jax.numpy as jnp  # pyrefly: ignore [import-error, missing-import]
    from jax.experimental import (  # pyrefly: ignore [import-error, missing-import]
        pallas as pl,
    )

    nonzero_rank_shape = shape if len(shape) > 0 else (1,)
    return pl.BlockSpec(
        nonzero_rank_shape,
        lambda i: [jnp.int32(i)] * len(nonzero_rank_shape),
    )

