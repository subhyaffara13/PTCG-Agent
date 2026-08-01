
def maybe_mark_dynamic_helper(t: torch.Tensor, dims: set[int]) -> None:
    if hasattr(t, "_dynamo_weak_dynamic_indices"):
        # pyrefly: ignore [missing-attribute]
        t._dynamo_weak_dynamic_indices |= dims
    else:
        t._dynamo_weak_dynamic_indices = dims.copy()  # type: ignore[attr-defined]

