
def from_fun(t: object) -> object:
    if isinstance(t, Tensor) and is_traceable_wrapper_subclass(t):
        # See Note [Functionalization always runs last]
        # This means that if we want to "functionalize" a subclass, we need to ensure that the functional wrapper
        # goes at the bottom.
        # recurse here, so we can support nested wrapper subclasses
        out = transform_subclass(t, lambda _, inner_t: from_fun(inner_t))
        torch._mirror_autograd_meta_to(t, out)  # type: ignore[attr-defined]
        return out

    if not isinstance(t, FunctionalTensor):
        # quick sanity assert
        if isinstance(t, torch.Tensor):
            if torch._is_functional_tensor(t):  # type: ignore[attr-defined]
                raise AssertionError("expected non-functional tensor")
        return t
    sync_functional_tensor(t)
    return torch._from_functional_tensor(t.elem)

