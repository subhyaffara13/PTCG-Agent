
def _get_storage_changed_counter(t: torch.Tensor) -> int:
    return sc_visit(
        t,
        lambda t: torch._functionalize_storage_changed_counter(t.elem),  # type: ignore[attr-defined]
        lambda l, r: max(l, r),
        -1,
    )

