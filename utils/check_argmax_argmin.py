
def check_argmax_argmin(name, self, dim):
    if dim is not None:
        dim = maybe_wrap_dim(dim, self.dim())
        zero_numel_check_dims(self, dim, name)
    else:
        torch._check(
            self.numel() != 0,
            lambda: f"{name}: Expected reduction dim to be specified for input.numel() == 0.",
        )

