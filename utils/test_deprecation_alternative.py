
def test_deprecation_alternative() -> None:
    alternative = "`.f1`, `f2`, `f3(x) <.f3>` or `f4(x)<f4>`"
    @_api.deprecated("1", alternative=alternative)
    def f() -> None:
        pass
    if f.__doc__ is None:
        pytest.skip('Documentation is disabled')
    assert alternative in f.__doc__

