
def sliding_window_bidirectional_overlay(sliding_window: int) -> Callable:
    """
    This is an overlay depicting a bidirectional sliding window pattern.
    """

    def inner_mask(batch_idx: int, head_idx: int, q_idx: int, kv_idx: int) -> bool:
        """A token can attend to any other token if their absolute distance is within
        the (inclusive) sliding window size (distance <= sliding_window)."""
        return abs(q_idx - kv_idx) <= sliding_window

    return inner_mask

