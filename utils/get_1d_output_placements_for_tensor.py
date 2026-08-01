
def get_1d_output_placements_for_tensor(t: torch.Tensor) -> list[Placement]:
    """
    Get all possible 1-D mesh placements for an OUTPUT tensor.
    """
    placements: list[Placement] = [Replicate()]
    for dim in range(t.ndim):
        placements.append(Shard(dim))

    if t.dtype != torch.bool:
        for reduce_op in PARTIAL_REDUCE_OPS:
            placements.append(Partial(reduce_op))
    return placements

