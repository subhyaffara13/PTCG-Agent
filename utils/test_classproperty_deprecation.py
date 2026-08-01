
def test_classproperty_deprecation() -> None:
    class A:
        @_api.deprecated("0.0.0")
        @_api.classproperty
        def f(cls: Self) -> None:
            pass
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        A.f
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        a = A()
        a.f

