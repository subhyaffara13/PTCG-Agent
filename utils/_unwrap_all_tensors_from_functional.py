
def _unwrap_all_tensors_from_functional(
    tensor_pytree: Any, *, reapply_views: bool
) -> Any:
    return tree_map(
        lambda t: _maybe_unwrap_functional_tensor(t, reapply_views=reapply_views),
        tensor_pytree,
    )

