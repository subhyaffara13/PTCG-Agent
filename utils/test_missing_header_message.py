
def test_missing_header_message():
    """Trying convert `list` to a `std::vector`, or vice versa, without including
    <pybind11/stl.h> should result in a helpful suggestion in the error message"""
    import pybind11_cross_module_tests as cm

    expected_message = (
        "Did you forget to `#include <pybind11/stl.h>`? Or <pybind11/complex.h>,\n"
        "<pybind11/functional.h>, <pybind11/chrono.h>, etc. Some automatic\n"
        "conversions are optional and require extra headers to be included\n"
        "when compiling your pybind11 module."
    )

    with pytest.raises(TypeError) as excinfo:
        cm.missing_header_arg([1.0, 2.0, 3.0])
    assert expected_message in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        cm.missing_header_return()
    assert expected_message in str(excinfo.value)

