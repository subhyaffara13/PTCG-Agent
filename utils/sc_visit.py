
def sc_visit(
    t: torch.Tensor,
    fn: Callable[[Tensor], T],
    reduce_fn: Callable[[T, T], T],
    accum_init: T,
) -> T:
    if not is_traceable_wrapper_subclass(t):
        return fn(t)

    accum = accum_init

    def visit(e: Any) -> None:
        if not is_traceable_wrapper_subclass(e):
            nonlocal accum
            accum = reduce_fn(accum, fn(e))
            return

        for a in e.__tensor_flatten__()[0]:
            match getattr(e, a):
                case torch.Tensor() as inner:
                    visit(inner)
                case OpaqueBase():
                    pass
                case unexpected:
                    raise AssertionError(
                        f"expected Tensor or OpaqueBase, got {type(unexpected)}"
                    )

    visit(t)
    return accum

