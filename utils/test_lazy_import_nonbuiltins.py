
def test_lazy_import_nonbuiltins():
    sp = lazy._lazy_import("scipy")
    np = lazy._lazy_import("numpy")
    if isinstance(sp, lazy.DelayedImportErrorModule):
        try:
            sp.special.erf
            assert False
        except ModuleNotFoundError:
            pass
    elif isinstance(np, lazy.DelayedImportErrorModule):
        try:
            np.sin(np.pi)
            assert False
        except ModuleNotFoundError:
            pass
    else:
        assert sp.special.erf(np.pi) == pytest.approx(1, 1e-4)

