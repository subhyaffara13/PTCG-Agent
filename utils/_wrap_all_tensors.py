
def _wrap_all_tensors(tensor_pytree: _T, level: int) -> _T:
    return tree_map(partial(_wrap_tensor_for_grad, level=level), tensor_pytree)

