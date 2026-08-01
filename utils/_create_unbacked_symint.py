
def _create_unbacked_symint(
    fake_mode: FakeTensorMode, ignore_fresh_unbacked_symbols: bool
) -> torch.SymInt:
    if fake_mode is None or fake_mode.shape_env is None:
        raise AssertionError("Must provide a fake_mode with shape_env.")
    ctx = (
        contextlib.nullcontext()
        if not ignore_fresh_unbacked_symbols
        else fake_mode.shape_env.ignore_fresh_unbacked_symbols()
    )
    with ctx:
        return fake_mode.shape_env.create_unbacked_symint()

