
def _batch_p2p_ops_meta(op_list, peer_list, tag_list, tensors, group_name):
    return [
        t if op == "irecv" else torch.empty(0, dtype=t.dtype, device=t.device)
        for op, t in zip(op_list, tensors)
    ]

