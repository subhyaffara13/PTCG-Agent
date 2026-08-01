
def heavy_rpc_torchscript(tensor):
    for i in range(1, 100):
        tensor *= i
        tensor /= i + 1
    return 0

