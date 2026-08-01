
def test_cython_lapack_abi_stability():
    """No existing cython_lapack signature may change or disappear."""
    expected = _EXPECTED['scipy.linalg.cython_lapack']
    mod = importlib.import_module('scipy.linalg.cython_lapack')
    actual = _extract_capi(mod)
    errors = []
    for name, expected_sig in expected.items():
        if name not in actual:
            errors.append(
                f"REMOVED  {name!r} (was {expected_sig!r})"
            )
        elif actual[name] != expected_sig:
            errors.append(
                f"CHANGED  {name!r}\n"
                f"  expected: {expected_sig!r}\n"
                f"  actual:   {actual[name]!r}"
            )
    if errors:
        joined = '\n'.join(errors)
        pytest.fail(
            f"scipy.linalg.cython_lapack.__pyx_capi__ has {len(errors)} "
            f"ABI breakage(s):\n{joined}"
        )

