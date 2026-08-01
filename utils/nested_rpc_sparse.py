
def nested_rpc_sparse(dst):
    return rpc.rpc_sync(
        dst, torch.add, args=(build_sparse_tensor(), build_sparse_tensor())
    )

