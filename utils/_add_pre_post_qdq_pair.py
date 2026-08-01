
def _add_pre_post_qdq_pair(
    qdq_cmp: dict[str, dict[str, Sequence[numpy.ndarray]]],
    activation_name: str,
    pre_qdq_tensors: Sequence[numpy.ndarray] | None,
    post_qdq_tensors: Sequence[numpy.ndarray] | None,
) -> None:
    if post_qdq_tensors is not None and pre_qdq_tensors is not None:
        qdq_cmp[activation_name] = {}
        qdq_cmp[activation_name]["pre_qdq"] = pre_qdq_tensors
        qdq_cmp[activation_name]["post_qdq"] = post_qdq_tensors

