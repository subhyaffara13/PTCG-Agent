
def _check_fake_real_tensors(
    real_out: torch.Tensor,
    fake_out: FakeTensor,
    context: str = "",
    sizes: bool = True,
    strides: bool = False,
    storage_offset: bool = True,
    requires_grad: bool = True,
) -> None:
    if requires_grad:
        if real_out.requires_grad != fake_out.requires_grad:
            raise MetadataMismatchError(
                f"{context} mismatched requires_grad-ness of outputs. "
                f"This usually means that you have added autograd support "
                f"for your operator at a dispatch key other than Autograd, "
                f"which will lead to problems"
            )

    if torch._C._has_storage(real_out):
        r_offset = real_out.storage_offset()
        f_offset = fake_out.storage_offset()
        if r_offset != f_offset:
            raise MetadataMismatchError(f"{context} mismatched storage offset")

    torch._prims.utils.compare_tensor_meta(
        real_out,
        fake_out,
        check_sizes=sizes,
        check_strides=strides,
        allow_rhs_unbacked=True,
    )

