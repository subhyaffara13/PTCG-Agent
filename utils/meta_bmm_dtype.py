
def meta_bmm_dtype(self, mat2, out_dtype):
    return common_meta_baddbmm_bmm(self, mat2, True, out_dtype=out_dtype)

