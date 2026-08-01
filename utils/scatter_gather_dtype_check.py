
def scatter_gather_dtype_check(method_name, self, index, src_opt=None):
    from torch.fx.experimental.symbolic_shapes import guard_or_true

    if guard_or_true(index.numel() != 0):
        torch._check(
            index.dtype == torch.long or index.dtype == torch.int,
            lambda: f"{method_name}(): Expected dtype int32/int64 for index",
        )

    if src_opt is not None:
        torch._check(
            self.dtype == src_opt.dtype,
            lambda: f"{method_name}(): Expected self.dtype to be equal to src.dtype",
        )

