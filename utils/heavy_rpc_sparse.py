
def heavy_rpc_sparse(tensor):
    for i in range(1, 100):
        tensor *= i
        tensor = tensor / (i + 1)
    return 0

