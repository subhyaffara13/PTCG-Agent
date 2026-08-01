
def window_partition(hidden_states, window_size):
    """
    Returns the resized hidden states. The output shape should be `(batch_size * num_windows, window_size, window_size,
    num_channels)`

    Args:
        hidden_states (`torch.FloatTensor` of shape `(batch_size, height, width, num_channels)`):
            Input hidden states
        window_size (`int`):
            Window size
    """
    batch_size, height, width, num_channels = hidden_states.shape

    hidden_states = hidden_states.view(
        batch_size, height // window_size, window_size, width // window_size, window_size, num_channels
    )
    windows = hidden_states.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, window_size, window_size, num_channels)
    return windows


def window_partition(input_feature, window_size):
    """
    Partitions the given input into windows.
    """
    batch_size, height, width, num_channels = input_feature.shape
    input_feature = input_feature.view(
        batch_size, height // window_size, window_size, width // window_size, window_size, num_channels
    )
    windows = input_feature.transpose(2, 3).contiguous().view(-1, window_size, window_size, num_channels)
    return windows


def window_partition(hidden_state, window_size):
    """
    Partition into non-overlapping windows with padding if needed.

    Args:
        hidden_state (`torch.Tensor`):
            Input tokens with [batch_size, height, width, num_channels].
        window_size (`int`):
            Window size.

    Returns:
        `tuple(torch.FloatTensor)` comprising various elements:
        - windows: windows after partition with [batch_size * num_windows, window_size, window_size, num_channels].
        - (padded_height, padded_width): padded height and width before partition
    """
    batch_size, height, width, num_channels = hidden_state.shape

    pad_height = (window_size - height % window_size) % window_size
    pad_width = (window_size - width % window_size) % window_size

    # Noop in case pad_width == 0 and pad_height == 0.
    hidden_state = nn.functional.pad(hidden_state, (0, 0, 0, pad_width, 0, pad_height))

    padded_height, padded_width = height + pad_height, width + pad_width

    hidden_state = hidden_state.view(
        batch_size, padded_height // window_size, window_size, padded_width // window_size, window_size, num_channels
    )
    windows = hidden_state.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, window_size, window_size, num_channels)
    return windows, (padded_height, padded_width)


def window_partition(input_feature, window_size):
    """
    Partitions the given input into windows.
    """
    batch_size, height, width, num_channels = input_feature.shape
    input_feature = input_feature.view(
        batch_size, height // window_size, window_size, width // window_size, window_size, num_channels
    )
    windows = input_feature.transpose(2, 3).contiguous().view(-1, window_size, window_size, num_channels)
    return windows


def window_partition(hidden_state, window_size):
    """
    Partition into non-overlapping windows with padding if needed.

    Args:
        hidden_state (`torch.Tensor`):
            Input tokens with [batch_size, height, width, num_channels].
        window_size (`int`):
            Window size.

    Returns:
        `tuple(torch.FloatTensor)` comprising various elements:
        - windows: windows after partition with [batch_size * num_windows, window_size, window_size, num_channels].
        - (padded_height, padded_width): padded height and width before partition
    """
    batch_size, height, width, num_channels = hidden_state.shape

    pad_height = (window_size - height % window_size) % window_size
    pad_width = (window_size - width % window_size) % window_size

    # Noop in case pad_width == 0 and pad_height == 0.
    hidden_state = nn.functional.pad(hidden_state, (0, 0, 0, pad_width, 0, pad_height))

    padded_height, padded_width = height + pad_height, width + pad_width

    hidden_state = hidden_state.view(
        batch_size, padded_height // window_size, window_size, padded_width // window_size, window_size, num_channels
    )
    windows = hidden_state.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, window_size, window_size, num_channels)
    return windows, (padded_height, padded_width)


def window_partition(hidden_state, window_size):
    """
    Partition into non-overlapping windows with padding if needed.

    Args:
        hidden_state (`torch.Tensor`):
            Input tokens with [batch_size, height, width, num_channels].
        window_size (`int`):
            Window size.

    Returns:
        `tuple(torch.FloatTensor)` comprising various elements:
        - windows: windows after partition with [batch_size * num_windows, window_size, window_size, num_channels].
        - (padded_height, padded_width): padded height and width before partition
    """
    batch_size, height, width, num_channels = hidden_state.shape
    pad_height = (window_size - height % window_size) % window_size
    pad_width = (window_size - width % window_size) % window_size

    # Noop in case pad_width == 0 and pad_height == 0.
    hidden_state = nn.functional.pad(hidden_state, (0, 0, 0, pad_width, 0, pad_height))

    padded_height, padded_width = height + pad_height, width + pad_width

    hidden_state = hidden_state.view(
        batch_size, padded_height // window_size, window_size, padded_width // window_size, window_size, num_channels
    )
    windows = hidden_state.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, window_size, window_size, num_channels)
    return windows, (padded_height, padded_width)


def window_partition(input_feature, window_size):
    """
    Partitions the given input into windows.
    """
    batch_size, height, width, num_channels = input_feature.shape
    input_feature = input_feature.view(
        batch_size, height // window_size, window_size, width // window_size, window_size, num_channels
    )
    windows = input_feature.transpose(2, 3).contiguous().view(-1, window_size, window_size, num_channels)
    return windows


def window_partition(input_feature, window_size):
    """
    Partitions the given input into windows.
    """
    batch_size, height, width, num_channels = input_feature.shape
    input_feature = input_feature.view(
        batch_size, height // window_size, window_size, width // window_size, window_size, num_channels
    )
    windows = input_feature.transpose(2, 3).contiguous().view(-1, window_size, window_size, num_channels)
    return windows


def window_partition(input_feature, window_size):
    """
    Partitions the given input into windows.
    """
    batch_size, height, width, num_channels = input_feature.shape
    input_feature = input_feature.view(
        batch_size, height // window_size, window_size, width // window_size, window_size, num_channels
    )
    windows = input_feature.transpose(2, 3).contiguous().view(-1, window_size, window_size, num_channels)
    return windows


def window_partition(input_feature, window_size):
    """
    Partitions the given input into windows.
    """
    batch_size, height, width, num_channels = input_feature.shape
    input_feature = input_feature.view(
        batch_size, height // window_size, window_size, width // window_size, window_size, num_channels
    )
    windows = input_feature.transpose(2, 3).contiguous().view(-1, window_size, window_size, num_channels)
    return windows


def window_partition(hidden_state, window_size):
    """
    Partition into non-overlapping windows with padding if needed.

    Args:
        hidden_state (`torch.Tensor`):
            Input tokens with [batch_size, height, width, num_channels].
        window_size (`int`):
            Window size.

    Returns:
        `tuple(torch.FloatTensor)` comprising various elements:
        - windows: windows after partition with [batch_size * num_windows, window_size, window_size, num_channels].
        - (padded_height, padded_width): padded height and width before partition
    """
    batch_size, height, width, num_channels = hidden_state.shape

    pad_height = (window_size - height % window_size) % window_size
    pad_width = (window_size - width % window_size) % window_size

    # Noop in case pad_width == 0 and pad_height == 0.
    hidden_state = nn.functional.pad(hidden_state, (0, 0, 0, pad_width, 0, pad_height))

    padded_height, padded_width = height + pad_height, width + pad_width

    hidden_state = hidden_state.view(
        batch_size, padded_height // window_size, window_size, padded_width // window_size, window_size, num_channels
    )
    windows = hidden_state.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, window_size, window_size, num_channels)
    return windows, (padded_height, padded_width)

