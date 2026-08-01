
def _get_default_structured_pruning_patterns() -> dict[
    tuple[type[nn.Module] | Callable | MatchAllNode | str, ...],
    Callable[..., None],
]:
    """
    Returns the patterns for conv2d / linear conversion for each element in the activation functions/modules defined above.
    """
    patterns: dict[
        tuple[type[nn.Module] | Callable | MatchAllNode | str, ...],
        Callable[..., None],
    ] = {
        # linear -> linear
        (nn.Linear, "output"): prune_linear,
        (nn.Linear, nn.Linear): prune_linear_linear,
        # conv2d -> conv2d
        (nn.Conv2d, "output"): prune_conv2d,
        (nn.Conv2d, nn.Conv2d): prune_conv2d_conv2d,
        # TODO LSTM Structured pruning does not support returned state currently.
        # Should find a way to explicitly match getitem(0) instead of getitem.
        # This will also require changing the pruning function.
        # lstm -> getitem(0) -> linear
        (nn.LSTM, getitem, nn.Linear): prune_lstm_output_linear,
        # lstm -> getitem(0) -> layernorm -> linear
        (nn.LSTM, getitem, nn.LayerNorm, nn.Linear): prune_lstm_output_layernorm_linear,
    }

    for activation in chain(
        _get_supported_activation_functions(), _get_supported_activation_modules()
    ):
        patterns.update(
            {
                # linear -> activation -> linear
                (nn.Linear, activation, nn.Linear): prune_linear_activation_linear,
                # conv2d -> activation -> conv2d
                (nn.Conv2d, activation, nn.Conv2d): prune_conv2d_activation_conv2d,
                # conv2d -> activation -> pool -> conv2d
                (
                    nn.Conv2d,
                    activation,
                    nn.AvgPool2d,
                    nn.Conv2d,
                ): prune_conv2d_activation_pool_conv2d,
                (
                    nn.Conv2d,
                    activation,
                    F.avg_pool2d,
                    nn.Conv2d,
                ): prune_conv2d_activation_pool_conv2d,
                (
                    nn.Conv2d,
                    activation,
                    nn.MaxPool2d,
                    nn.Conv2d,
                ): prune_conv2d_activation_pool_conv2d,
                (
                    nn.Conv2d,
                    activation,
                    F.max_pool2d,
                    nn.Conv2d,
                ): prune_conv2d_activation_pool_conv2d,
                # conv2d -> pool -> activation -> conv2d
                (
                    nn.Conv2d,
                    nn.AvgPool2d,
                    activation,
                    nn.Conv2d,
                ): prune_conv2d_pool_activation_conv2d,
                (
                    nn.Conv2d,
                    F.avg_pool2d,
                    activation,
                    nn.Conv2d,
                ): prune_conv2d_pool_activation_conv2d,
                (
                    nn.Conv2d,
                    nn.MaxPool2d,
                    activation,
                    nn.Conv2d,
                ): prune_conv2d_pool_activation_conv2d,
                (
                    nn.Conv2d,
                    F.max_pool2d,
                    activation,
                    nn.Conv2d,
                ): prune_conv2d_pool_activation_conv2d,
                # conv2d -> adaptive pool -> flatten -> linear
                (
                    nn.Conv2d,
                    nn.AdaptiveAvgPool2d,
                    nn.Flatten,
                    nn.Linear,
                ): prune_conv2d_pool_flatten_linear,
                (
                    nn.Conv2d,
                    nn.AdaptiveAvgPool2d,
                    torch.flatten,
                    nn.Linear,
                ): prune_conv2d_pool_flatten_linear,
                (
                    nn.Conv2d,
                    nn.AdaptiveMaxPool2d,
                    nn.Flatten,
                    nn.Linear,
                ): prune_conv2d_pool_flatten_linear,
                (
                    nn.Conv2d,
                    nn.AdaptiveMaxPool2d,
                    torch.flatten,
                    nn.Linear,
                ): prune_conv2d_pool_flatten_linear,
            }
        )
    return patterns

