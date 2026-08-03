from typing import Any

def _view_meta(
    fake_mode: FakeTensorMode,
    func: OpOverload,
    a: FakeTensor,
    *shape: Any,
    allow_copy: bool = False,
) -> FakeTensor:
    if torch.fx.experimental._config.backed_size_oblivious or _view_has_unbacked_input(
        a, shape
    ):
        return typing_cast(
            FakeTensor, _view_unbacked_meta(a, shape, allow_copy=allow_copy)
        )
    else:
        return typing_cast(
            FakeTensor,
            torch._refs._reshape_view_helper(a, *shape, allow_copy=allow_copy),
        )

