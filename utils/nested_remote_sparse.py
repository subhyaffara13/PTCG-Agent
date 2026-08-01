
def nested_remote_sparse(dst):
    rref = rpc.remote(
        dst, torch.add, args=(build_sparse_tensor(), build_sparse_tensor())
    )
    return rref.to_here()

