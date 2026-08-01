
def context_add_using_tf32(context: AHContext, dtype: torch.dtype) -> None:
    using_tf32 = "not_float_32"
    if dtype == torch.float32:
        using_tf32 = torch.backends.cuda.matmul.fp32_precision == "tf32"
    context.add_feature("using_tf32", using_tf32, is_categorical=True)

