
def test_cython_api_completeness():
    # Check that everything is tested
    for name in dir(cython_special):
        func = getattr(cython_special, name)
        if callable(func) and not name.startswith('_'):
            for _, cyfun, _, _ in PARAMS:
                if cyfun is func:
                    break
            else:
                raise RuntimeError(f"{name} missing from tests!")

