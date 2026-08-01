
def _dtype_to_typestr(dtype):
    # CUDA devices are little-endian and tensors are stored in native byte
    # order. 1-byte entries are endian-agnostic.
    return {
        torch.complex64: "<c8",
        torch.complex128: "<c16",
        torch.bfloat16: "<V2",  # Same as ml_dtypes.bfloat16.dtype.str.
        torch.float16: "<f2",
        torch.float32: "<f4",
        torch.float64: "<f8",
        torch.uint8: "|u1",
        torch.int8: "|i1",
        torch.uint16: "<u2",
        torch.int16: "<i2",
        torch.uint32: "<u4",
        torch.int32: "<i4",
        torch.uint64: "<u8",
        torch.int64: "<i8",
        torch.bool: "|b1",
    }[dtype]

