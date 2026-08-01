
def test_cross_module_interleaved_error_already_set():
    with pytest.raises(RuntimeError) as excinfo:
        m.test_cross_module_interleaved_error_already_set()
    assert str(excinfo.value) in (
        "2nd error.",  # Almost all platforms.
        "RuntimeError: 2nd error.",  # Some PyPy builds (seen under macOS).
    )

