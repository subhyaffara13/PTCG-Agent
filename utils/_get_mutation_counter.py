
def _get_mutation_counter(t: torch.Tensor) -> int:
    return sc_visit(
        t,
        lambda t: torch._functionalize_mutation_counter(t.elem),  # type: ignore[attr-defined]
        lambda l, r: max(l, r),
        -1,
    )

