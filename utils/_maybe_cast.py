
def _maybe_cast(x: Tensor | None, dtype) -> Tensor | None:
    if x is not None:
        return x.to(dtype)
    return x

