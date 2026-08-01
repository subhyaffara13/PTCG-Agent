
def _category(dtype):
    return {
        torch.bool: 0,
        torch.SymBool: 0,
        # int
        torch.uint8: 1,
        torch.int8: 1,
        torch.int16: 1,
        torch.int32: 1,
        torch.int64: 1,
        torch.SymInt: 1,
        # float
        torch.float16: 2,
        torch.float32: 2,
        torch.float64: 2,
        torch.SymFloat: 2,
        # complex
        torch.complex64: 3,
        torch.complex128: 3,
    }[dtype]

