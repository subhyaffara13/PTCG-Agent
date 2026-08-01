
def shift_dtype_check(fn_name, self, val):
    torch._check(
        utils.is_integer_dtype(self.dtype),
        lambda: f"{fn_name}: Expected input tensor to have an integral dtype. Got {self.dtype}",
    )
    if isinstance(val, torch.Tensor):
        torch._check(
            utils.is_integer_dtype(val.dtype),
            lambda: f"{fn_name}: Expected shift value to have an integral dtype. Got {val.dtype}",
        )
    else:
        torch._check(
            isinstance(val, IntLike),
            lambda: f"{fn_name}: Expected shift value to be an int. Got {val}",
        )

