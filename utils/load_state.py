
def load_state(
    model: nn.Module,
    weights: Sequence[Tensor],
    weight_names: Sequence[str],
    buffers: Sequence[Tensor] = (),
    buffer_names: Sequence[str] = (),
) -> nn.Module:
    """load_state(model, weights, weight_names, buffers=(), buffer_names=()) -> model

    load_state takes `weights` and `buffers` and assigns them to the model.
    This is the inverse operation of `make_functional_deprecated_v1`.
    """
    if len(weight_names) != len(weights):
        raise AssertionError(
            f"len(weight_names)={len(weight_names)} != len(weights)={len(weights)}"
        )
    load_weights(model, weight_names, weights)
    if len(buffers) > 0:
        if len(buffer_names) != len(buffers):
            raise AssertionError(
                f"len(buffer_names)={len(buffer_names)} != len(buffers)={len(buffers)}"
            )
        load_buffers(model, buffer_names, buffers)
    return model

