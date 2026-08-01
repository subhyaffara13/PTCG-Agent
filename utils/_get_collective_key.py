
def _get_collective_key(coll_node: fx.Node) -> str:
    """Extract a unique key for a collective node including group info and tensor size."""
    from torch._inductor import fx_utils

    opt_args_kwargs = normalize_function(
        coll_node.target,  # type: ignore[arg-type]
        args=coll_node.args,
        kwargs=coll_node.kwargs,
        normalize_to_only_use_kwargs=True,
    )
    assert opt_args_kwargs is not None
    _, kwargs = opt_args_kwargs
    group_name = kwargs.get("group_name", None)
    group_size = kwargs.get("group_size", None)

    tensor_bytes: int | None = None
    success, args, kw = fx_utils.get_fake_args_kwargs(coll_node)
    if success:

        def extract_first_tensor_bytes(t: torch.Tensor) -> torch.Tensor:
            nonlocal tensor_bytes
            if tensor_bytes is None:
                shape = [get_hint(dim) for dim in t.shape]
                if all(s is not None for s in shape):
                    numel = functools.reduce(operator.mul, shape, 1)
                    tensor_bytes = numel * t.dtype.itemsize
            return t

        torch.utils._pytree.tree_map_only(
            torch.Tensor, extract_first_tensor_bytes, (args, kw)
        )

    return f"{coll_node.target} group_size:{group_size} group_name:{group_name} input_bytes:{tensor_bytes}"

