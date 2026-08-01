
def _is_int8_mat(mat):
    return mat.get_dtype() in (torch.int8, torch.uint8)

