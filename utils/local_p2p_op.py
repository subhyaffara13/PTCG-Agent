
def local_p2p_op(
    dst: torch.SymInt,
    tensor: torch.Tensor,
    op: Callable[[torch.Tensor, int], Work | None],
) -> Work | list[Work | None] | None:
    """
    Runs a point-to-point (P2P) operation for all combinations of source and destination ranks.
    """
    _check_op(op)

    from . import LocalIntNode

    if not isinstance(dst.node, LocalIntNode):
        raise AssertionError(
            "Expected 'dst' to be a LocalIntNode where the value is the "
            "destination rank and key is the source rank"
        )

    w = []
    for s, d in dst.node._local_ints.items():
        tensor = _attach_rank(tensor, s)
        w.append(op(tensor, d))
    return w

