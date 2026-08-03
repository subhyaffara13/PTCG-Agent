from typing import Callable

def _vmap_expansion_sdpa(mask_function: Callable) -> Callable:
    """
    Used to vmap our mask_functions over the all 4 dimensions (b_idx, h_idx, q_idx, kv_idx) of the inputs.
    Using vmap here allows us to keep the performance of vectorized ops, while having a single set of primitive
    functions between attention interfaces (i.e. between flex and sdpa/eager, FA2 being a bit different).
    """
    # We vmap the function over all 4 dimensions, broadcasting [b_idx, h_idx, q_idx, kv_idx]
    dimensions = [(None, None, None, 0), (None, None, 0, None), (None, 0, None, None), (0, None, None, None)]
    for dims in dimensions:
        mask_function = torch.vmap(mask_function, in_dims=dims, out_dims=0)
    return mask_function

