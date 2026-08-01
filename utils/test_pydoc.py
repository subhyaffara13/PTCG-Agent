
def test_pydoc():
    """Pydoc needs to be able to provide help() for everything inside a pybind11 module"""
    import pydoc

    import pybind11_tests

    assert pybind11_tests.__name__ == "pybind11_tests"
    assert pybind11_tests.__doc__ == "pybind11 test module"
    assert pydoc.text.docmodule(pybind11_tests)

