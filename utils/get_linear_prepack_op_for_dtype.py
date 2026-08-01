
def get_linear_prepack_op_for_dtype(dtype):
    if dtype == torch.float16:
        return torch.ops.quantized.linear_prepack_fp16
    elif dtype == torch.qint8:
        return torch.ops.quantized.linear_prepack
    else:
        raise Exception("can't get linear prepack op for dtype:", dtype)  # noqa: TRY002

