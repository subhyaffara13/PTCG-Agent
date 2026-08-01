
def nested_rref_sparse(dst):
    return (
        rpc.remote(dst, torch.add, args=(build_sparse_tensor(), build_sparse_tensor())),
        rpc.remote(dst, torch.add, args=(build_sparse_tensor(), build_sparse_tensor())),
    )

