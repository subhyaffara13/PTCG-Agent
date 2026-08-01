
def assert_flat_tuple_of_tensors(elts: Any, api: str, argname: str) -> None:
    if not isinstance(elts, tuple):
        raise RuntimeError(
            f"{api}: Expected {argname} to be a tuple of Tensors, got {type(elts)}"
        )
    for elt in elts:
        if isinstance(elt, torch.Tensor):
            continue
        raise RuntimeError(
            f"{api}: Expected {argname} to be a tuple of Tensors, got "
            f"a tuple with an element of type {type(elt)}"
        )
    if len(elts) == 0:
        raise RuntimeError(
            f"{api}: Expected {argname} to be a non-empty tuple of Tensors."
        )

