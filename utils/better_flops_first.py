
def better_flops_first(flops: int, size: int, best_flops: int, best_size: int) -> bool:
    return (flops, size) < (best_flops, best_size)

