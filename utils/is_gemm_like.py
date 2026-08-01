
def is_gemm_like(node: IRNode | Operation | None) -> bool:
    if node is None:
        return False

    if is_fallback_op(
        node,  # type: ignore[arg-type]
        torch.ops.aten._scaled_dot_product_flash_attention.default,
    ):
        return True

    if (
        python_kernel_name := getattr(node, "python_kernel_name", None)
    ) and "extern_kernels" in python_kernel_name:
        return True
    return False

