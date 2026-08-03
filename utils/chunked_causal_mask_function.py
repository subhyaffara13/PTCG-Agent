from typing import Callable

def chunked_causal_mask_function(chunk_size: int, left_padding: torch.Tensor) -> Callable:
    """
    This return the mask_function function to create a chunked attention mask.
    """
    return and_masks(chunked_overlay(chunk_size, left_padding), causal_mask_function)

