
def validate_aten_combination(
    aten_op: OpOverload,
    captured_args: tuple[Any, ...],
    captured_kwargs: dict[str, Any],
    ground_truth: torch.Tensor | list[torch.Tensor],
    combination: PlacementCombination,
    world_size: int,
    mesh: DeviceMesh,
    mask_shift: int = 0,
) -> tuple[bool | None, str]:
    """Validate a placement combination using aten-level captured args.

    Works directly with aten op args/kwargs instead of SampleInput pytrees.
    Replaces tensors in the flat args/kwargs with sharded LocalTensors,
    calls the aten op, and compares output.

    Returns (True, ""), (False, error_msg), or (None, reason) if untestable.
    """
    try:
        tensors = extract_tensors_from_args(captured_args, captured_kwargs)
        if not tensors:
            return False, "No tensor args in captured aten call"

        for (name, tensor), placement in zip(tensors, combination[0]):
            if isinstance(placement, Shard):
                if tensor.size(placement.dim) % world_size != 0:
                    return None, "uneven shard"

        local_tensors = _shard_tensors(
            tensors, combination[0], world_size, mesh, mask_shift
        )

        local_idx = 0

        def _replace_with_local(a: Any) -> Any:
            nonlocal local_idx
            if isinstance(a, torch.Tensor):
                local = local_tensors[local_idx]
                local_idx += 1
                return local
            return a

        local_args = pytree.tree_map(_replace_with_local, captured_args)
        local_kwargs = pytree.tree_map(_replace_with_local, captured_kwargs)

        local_output = aten_op(*local_args, **local_kwargs)

        return _compare_outputs(
            local_output, ground_truth, combination[1], mesh, world_size
        )

    except Exception as e:
        return False, f"Exception: {type(e).__name__}: {e}"

