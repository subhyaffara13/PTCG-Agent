
def check_cat_no_zero_dim(tensors: list[list[int]]):
    for tensor in tensors:
        if len(tensor) <= 0:
            raise AssertionError("Cannot concatenate tensor with 0 dimensions")

