
def assert_no_mixed_partial_types(placements: Sequence[Placement]) -> None:
    """
    Assert that a placement list doesn't contain mixed Partial reduce types.

    Mixed Partial types (e.g., ``Partial("sum")`` and ``Partial("max")`` together in the
    same placement list) are not supported and will raise a ``ValueError``. This restriction
    exists because nonlinear reductions (e.g., max) don't commute with linear reductions
    (e.g., sum), which means the relative ordering of different partial types would be
    semantically critical during redistribution. Rather than introducing complex ordering
    constraints, we prohibit mixing different Partial reduce types.

    Note: Partial("sum") and Partial("avg") DO commute with each other, so they can be ordered
    arbitrarily, and we allow this.

    This function is called internally by public APIs like :meth:`DTensor.from_local` and
    :func:`distribute_tensor` to validate placements early, before DTensor construction.

    Args:
        placements (Sequence[:class:`Placement`]): A sequence of placement specifications
            to validate.

    Raises:
        ValueError: If the placements contain more than one distinct Partial reduce type.
    """
    partial_reduce_ops: set[str] = set()
    for p in placements:
        if isinstance(p, Partial):
            partial_reduce_ops.add(p.reduce_op)

    if len(partial_reduce_ops) > 1 and partial_reduce_ops != {"sum", "avg"}:
        raise ValueError(
            f"Mixed Partial reduce types are not supported in the same placement list. "
            f"Found reduce ops: {partial_reduce_ops}. "
            f"Please ensure all Partial placements use the same reduce operation."
        )

