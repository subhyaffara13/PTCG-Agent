
def zero_numel_check_dims(self, dim, fn_name):
    if self.ndim == 0:
        torch._check_index(
            dim == 0 or dim == -1,
            lambda: f"{fn_name}: Expected reduction dim -1 or 0 for scalar but got {dim}",
        )
    else:
        torch._check_index(
            self.size(dim) != 0,
            lambda: f"{fn_name}: Expected reduction dim {dim} to have non-zero size.",
        )

