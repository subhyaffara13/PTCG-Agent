
def pa():
    if not _HAVE_PYARROW:
        pytest.skip("pyarrow is not installed")
    return "pyarrow"

