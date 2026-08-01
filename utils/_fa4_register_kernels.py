
def _fa4_register_kernels() -> Library:
    lib = Library("aten", "IMPL", "CUDA")  # noqa: TOR901
    lib.impl("_flash_attention_forward", _fa4_flash_attention_forward_impl, "CUDA")
    lib.impl(
        "_flash_attention_forward_no_dropout_inplace",
        _fa4_flash_attention_forward_no_dropout_inplace_impl,
        "CUDA",
    )
    lib.impl("_flash_attention_backward", _fa4_flash_attention_backward_impl, "CUDA")
    lib.impl(
        "_scaled_dot_product_flash_attention",
        _fa4_scaled_dot_product_flash_attention_forward_impl,
        "CUDA",
    )
    lib.impl(
        "_scaled_dot_product_flash_attention_backward",
        _fa4_scaled_dot_product_flash_attention_backward_impl,
        "CUDA",
    )
    return lib

