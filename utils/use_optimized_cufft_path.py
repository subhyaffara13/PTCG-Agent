
def use_optimized_cufft_path(dim: list[int]):
    if len(dim) > cufft_max_ndim or (len(dim) >= 2 and dim[0] == 0 and dim[1] == 1):
        return False
    else:
        return True

