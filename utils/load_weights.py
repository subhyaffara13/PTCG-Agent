
def load_weights(
    mod: nn.Module,
    names: Sequence[str],
    params: Sequence[Tensor],
    as_params: bool = False,
) -> None:
    """
    Reload a set of weights so that `mod` can be used again to perform a forward pass.
    Note that the `params` are regular Tensors (that can have history) and so are left
    as Tensors. This means that mod.parameters() will still be empty after this call.
    """
    accessor = NamedMemberAccessor(mod)
    if as_params:
        params = [nn.Parameter(p) for p in params]
    accessor.set_tensors(names, params)

