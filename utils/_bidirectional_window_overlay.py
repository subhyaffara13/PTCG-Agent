
def _bidirectional_window_overlay(sliding_window: int) -> Callable[[int, int, int, int], bool]:
    """
    Enables a bidirectional mask within the sliding window.
    """

    def inner_mask(batch_idx: int, head_idx: int, q_idx: int, kv_idx: int) -> bool:
        """A token can attend to any other token if their absolute distance is within
        the (exclusive) sliding window size (distance < sliding_window)."""
        return abs(q_idx - kv_idx) < sliding_window

    return inner_mask


def _bidirectional_window_overlay(sliding_window: int) -> Callable[[int, int, int, int], bool]:
    """
    Enables a bidirectional mask within the sliding window.
    """

    def inner_mask(batch_idx: int, head_idx: int, q_idx: int, kv_idx: int) -> bool:
        """A token can attend to any other token if their absolute distance is within
        the (exclusive) sliding window size (distance < sliding_window)."""
        return abs(q_idx - kv_idx) < sliding_window

    return inner_mask

