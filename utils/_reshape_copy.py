from typing import Any

def _reshape_copy(
    fake_mode: FakeTensorMode, func: OpOverload, a: FakeTensor, *shape: Any
) -> FakeTensor | Exception:
    if a.is_sparse or a.is_mkldnn:
        return NotImplemented

    # pyrefly: ignore[bad-argument-count]
    shape = utils.infer_size(*shape, a.numel())
    if is_contiguous_or_false(a):
        view = _view_meta(fake_mode, func, a, *shape)
        return typing_cast(
            FakeTensor, view.clone(memory_format=torch.contiguous_format)
        )
    else:
        return _view_meta(
            fake_mode,
            func,
            typing_cast(FakeTensor, a.clone(memory_format=torch.contiguous_format)),
            *shape,
        )

