
def _unwrap_tensoralias(x: TensorAlias) -> torch.Tensor:
    if not isinstance(x, TensorAlias):
        raise AssertionError(f"expected TensorAlias, got {type(x)}")
    return x.alias

