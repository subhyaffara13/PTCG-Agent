
def _is_empty_2d(arr):
    # check size first for efficiency
    return arr.size == 0 and prod(arr.shape[-2:]) == 0

