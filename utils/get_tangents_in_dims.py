
def get_tangents_in_dims(input_dims: Any, tangents: tuple[Any, ...]) -> Any:
    flat_in_dims, spec = pytree.tree_flatten(input_dims)
    flat_tangents = pytree.arg_tree_leaves(*tangents)
    result = [
        None if tangent is None else in_dim
        for in_dim, tangent in zip(flat_in_dims, flat_tangents)
    ]
    return pytree.tree_unflatten(result, spec)

