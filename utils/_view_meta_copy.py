
def _view_meta_copy(
    fake_mode: FakeTensorMode,
    func: OpOverload,
    a: FakeTensor,
    *shape: IntLikeType,
    out: FakeTensor | None = None,
) -> FakeTensor:
    # view_copy is the non-aliasing counterpart of view. Eager may succeed on
    # cases where a pure view is impossible (e.g. expand -> flatten) by
    # materializing the result. Match eager by allowing copy-if-needed in meta.
    result = _view_meta(fake_mode, func, a, *shape, allow_copy=True)

    if out is not None:
        return result

    return pytree.tree_map(
        lambda x: x.clone(memory_format=torch.contiguous_format),
        result,
    )

