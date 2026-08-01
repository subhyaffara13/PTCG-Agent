
def _batch_p2p_ops(
    op_list: list[str],
    peer_list: list[int],
    tag_list: list[int],
    tensors: list[torch.Tensor],
    group_name: str,
):
    return torch.ops._c10d_functional.batch_p2p_ops(
        op_list, peer_list, tag_list, tensors, group_name
    )

