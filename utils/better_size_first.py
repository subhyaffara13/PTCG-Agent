
def better_size_first(flops: int, size: int, best_flops: int, best_size: int) -> bool:
    return (size, flops) < (best_size, best_flops)

