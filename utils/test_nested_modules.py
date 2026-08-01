
def test_nested_modules():
    import pybind11_tests

    assert pybind11_tests.__name__ == "pybind11_tests"
    assert pybind11_tests.modules.__name__ == "pybind11_tests.modules"
    assert (
        pybind11_tests.modules.subsubmodule.__name__
        == "pybind11_tests.modules.subsubmodule"
    )
    assert m.__name__ == "pybind11_tests.modules"
    assert ms.__name__ == "pybind11_tests.modules.subsubmodule"

    assert ms.submodule_func() == "submodule_func()"

