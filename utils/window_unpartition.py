
def window_unpartition(windows, window_size, pad_height_width, height_width):
    """
    Window unpartition into original sequences and removing padding.

    Args:
        windows (`torch.Tensor`):
            Input tokens with [batch_size * num_windows, window_size, window_size, num_channels].
        window_size (`int`):
            Window size.
        pad_height_width (`tuple[int]`):
            Padded height and width (padded_height, padded_width).
        height_width (`tuple[int]`):
            Original height and width before padding.

    Returns:
        hidden_state: unpartitioned sequences with [batch_size, height, width, num_channels].
    """
    padded_height, padded_width = pad_height_width
    height, width = height_width
    batch_size = windows.shape[0] // (padded_height * padded_width // window_size // window_size)
    hidden_state = windows.view(
        batch_size, padded_height // window_size, padded_width // window_size, window_size, window_size, -1
    )
    hidden_state = hidden_state.permute(0, 1, 3, 2, 4, 5).contiguous()
    hidden_state = hidden_state.view(batch_size, padded_height, padded_width, -1)

    # We always have height <= padded_height and width <= padded_width
    hidden_state = hidden_state[:, :height, :width, :].contiguous()
    return hidden_state


def window_unpartition(windows, window_size, pad_height_width, height_width):
    """
    Window unpartition into original sequences and removing padding.

    Args:
        windows (`torch.Tensor`):
            Input tokens with [batch_size * num_windows, window_size, window_size, num_channels].
        window_size (`int`):
            Window size.
        pad_height_width (`tuple[int]`):
            Padded height and width (padded_height, padded_width).
        height_width (`tuple[int]`):
            Original height and width before padding.

    Returns:
        hidden_state: unpartitioned sequences with [batch_size, height, width, num_channels].
    """
    padded_height, padded_width = pad_height_width
    height, width = height_width
    batch_size = windows.shape[0] // (padded_height * padded_width // window_size // window_size)
    hidden_state = windows.view(
        batch_size, padded_height // window_size, padded_width // window_size, window_size, window_size, -1
    )
    hidden_state = hidden_state.permute(0, 1, 3, 2, 4, 5).contiguous()
    hidden_state = hidden_state.view(batch_size, padded_height, padded_width, -1)

    # We always have height <= padded_height and width <= padded_width
    hidden_state = hidden_state[:, :height, :width, :].contiguous()
    return hidden_state


def window_unpartition(windows, window_size, pad_height_width, height_width):
    """
    Window unpartition into original sequences and removing padding.

    Args:
        windows (`torch.Tensor`):
            Input tokens with [batch_size * num_windows, window_size, window_size, num_channels].
        window_size (`int`):
            Window size.
        pad_height_width (`tuple[int]`):
            Padded height and width (padded_height, padded_width).
        height_width (`tuple[int]`):
            Original height and width before padding.

    Returns:
        hidden_state: unpartitioned sequences with [batch_size, height, width, num_channels].
    """
    padded_height, padded_width = pad_height_width
    height, width = height_width
    batch_size = windows.shape[0] // (padded_height * padded_width // window_size // window_size)
    hidden_state = windows.view(
        batch_size, padded_height // window_size, padded_width // window_size, window_size, window_size, -1
    )
    hidden_state = hidden_state.permute(0, 1, 3, 2, 4, 5).contiguous()
    hidden_state = hidden_state.view(batch_size, padded_height, padded_width, -1)

    # We always have height <= padded_height and width <= padded_width
    hidden_state = hidden_state[:, :height, :width, :].contiguous()
    return hidden_state

