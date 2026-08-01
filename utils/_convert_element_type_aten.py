
def _convert_element_type_aten(a: Tensor, dtype: torch.dtype) -> Tensor:
    # Propagates requires grad when possible
    if not utils.is_grad_dtype(dtype):
        requires_grad = False
    else:
        # TODO: update meta objects so this can be acquired directly
        try:
            requires_grad = a.requires_grad
        except Exception:
            requires_grad = False

    result = torch.empty_like(
        a, device=a.device, dtype=dtype, requires_grad=requires_grad
    )
    with torch.no_grad():
        return copy_to(result, a)

