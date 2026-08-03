from typing import Callable

def sliding_window_bidirectional_mask_function(sliding_window: int) -> Callable:
    """
    This return the mask_function function to create a bidirectional sliding window mask.
    """
    return and_masks(sliding_window_bidirectional_overlay(sliding_window), bidirectional_mask_function)

