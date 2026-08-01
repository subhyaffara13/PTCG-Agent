
def _any_differentiable(
    tensor_or_tuple_of_tensors: _Tensors,
) -> bool:
    flat_args, _ = tree_flatten(tensor_or_tuple_of_tensors)
    return any(tuple(map(_is_differentiable, flat_args)))

