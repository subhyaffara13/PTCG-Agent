from typing import Any

def _maybe_fake_tracing(fn, inputs: list[Any], pre_dispatch):
    fake_mode_det = None
    for inp in pytree.tree_leaves(inputs):
        if isinstance(inp, FakeTensor):
            fake_mode_det = inp.fake_mode
            break

    fake_mode: AbstractContextManager = nullcontext()
    tracing_mode = "fake"
    if fake_mode_det is not None:
        fake_mode = fake_mode_det
        tracing_mode = "real"

    # Note: we need to turn off proxy tensor mode to avoid tracing infra
    # code that happens in make_fx e.g. we now call as_strided when wrapping tensor
    # as fake tensor.
    with fake_mode, disable_proxy_modes_tracing():
        gm = make_fx(
            fn,
            tracing_mode=tracing_mode,
            pre_dispatch=pre_dispatch,
            _error_on_data_dependent_ops=False,
        )(*inputs)
        if not isinstance(fake_mode, nullcontext) and fake_mode.shape_env is not None:  # type: ignore[attr-defined]
            insert_deferred_runtime_asserts(
                gm,
                fake_mode.shape_env,  # type: ignore[attr-defined]
                "hoo_maybe_fake_tracing",
                export=True,  # type: ignore[attr-defined]
            )
        return gm

