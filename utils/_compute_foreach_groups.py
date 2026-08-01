
def _compute_foreach_groups(
    ag_ins: list[torch.Tensor],
    out_dtypes: list[torch.dtype],  # type: ignore[name-defined]
) -> list[int] | None:
    """
    Compute groups of indices that have the same src/dst dtype and shape.

    Groups tensors by (src_dtype, dst_dtype, shape) to avoid falling back to the foreach slow path.

    Returns a flat list with -1 as group delimiter, or None if only one group exists.
    For example, groups [[0, 2], [1]] would be encoded as [0, 2, -1, 1].
    """
    from torch.fx.experimental.symbolic_shapes import guarding_hint_or_throw

    groups: defaultdict[tuple[torch.dtype, torch.dtype, tuple[int, ...]], list[int]] = (
        defaultdict(list)
    )
    for i, (ag_in, out_dtype) in enumerate(zip(ag_ins, out_dtypes)):
        shape = tuple(guarding_hint_or_throw(s) for s in ag_in.shape)
        key = (ag_in.dtype, out_dtype, shape)
        groups[key].append(i)

    if len(groups) <= 1:
        return None

    # Encode as flat list with -1 as delimiter
    result: list[int] = []
    for i, group_indices in enumerate(groups.values()):
        result.extend(group_indices)
        if i < len(groups) - 1:
            result.append(-1)

    return result

