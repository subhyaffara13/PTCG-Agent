
def test_fallback_to_different_backend():
    pytest.importorskip("IPython")
    # Runs the process that caused the GH issue 23770
    # making sure that this doesn't crash
    # since we're supposed to be switching to a different backend instead.
    response = _run_helper(_fallback_check, timeout=_test_timeout)

