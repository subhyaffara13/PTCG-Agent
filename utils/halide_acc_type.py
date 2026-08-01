
def halide_acc_type(dtype):
    if is_integer_dtype(dtype) and dtype.is_signed and dtype != torch.int64:
        dtype = torch.int32
    if dtype in (torch.float16, torch.bfloat16):
        dtype = torch.float32
    return halide_type(dtype)

