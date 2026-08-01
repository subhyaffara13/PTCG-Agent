
def test_delete_parameter() -> None:
    @_api.delete_parameter("3.0", "foo")
    def func1(foo: Any = None) -> None:
        pass

    @_api.delete_parameter("3.0", "foo")
    def func2(**kwargs: Any) -> None:
        pass

    for func in [func1, func2]:  # type: ignore[list-item]
        func()  # No warning.
        with pytest.warns(mpl.MatplotlibDeprecationWarning):
            func(foo="bar")

    def pyplot_wrapper(foo: Any = _api.deprecation._deprecated_parameter) -> None:
        func1(foo)

    pyplot_wrapper()  # No warning.
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        func(foo="bar")

