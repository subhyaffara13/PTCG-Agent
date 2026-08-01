
def tag_to_layout_constraint(
    tag: torch._C.Tag,
) -> Callable[..., tuple[Any, Any]] | None:
    if tag == torch._C.Tag.needs_exact_strides:
        return constrain_to_fake_tensors
    if tag == torch._C.Tag.needs_contiguous_strides:  # type: ignore[attr-defined]
        return require_contiguous_strides
    if tag == torch._C.Tag.needs_fixed_stride_order:
        return constrain_to_fx_strides
    if tag == torch._C.Tag.flexible_layout:
        return None
    raise AssertionError(f"Unknown layout constraint tag: {tag}")

