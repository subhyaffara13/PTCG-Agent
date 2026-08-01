
def _fa3_register_kernels() -> Library:
    lib = Library("aten", "IMPL", "CUDA")  # noqa: TOR901
    lib.impl(
        "_flash_attention_forward.quantized", _fa3_flash_attention_forward_impl, "CUDA"
    )
    lib.impl(
        "_scaled_dot_product_flash_attention.quantized",
        _fa3_scaled_dot_product_flash_attention_forward_impl,
        "CUDA",
    )
    lib.impl(
        "_flash_attention_forward", _fa3_flash_attention_forward_impl_default, "CUDA"
    )
    lib.impl(
        "_flash_attention_forward_no_dropout_inplace",
        _fa3_flash_attention_forward_no_dropout_inplace_impl,
        "CUDA",
    )
    lib.impl(
        "_scaled_dot_product_flash_attention",
        _fa3_scaled_dot_product_flash_attention_forward_impl_default,
        "CUDA",
    )

    lib.impl("_flash_attention_backward", _fa3_flash_attention_backward_impl, "CUDA")
    lib.impl(
        "_scaled_dot_product_flash_attention_backward",
        _fa3_scaled_dot_product_flash_attention_backward_impl,
        "CUDA",
    )
    return lib

