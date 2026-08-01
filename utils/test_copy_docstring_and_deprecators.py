
def test_copy_docstring_and_deprecators(recwarn):
    @mpl._api.rename_parameter(mpl.__version__, "old", "new")
    @mpl._api.make_keyword_only(mpl.__version__, "kwo")
    def func(new, kwo=None):
        pass

    @plt._copy_docstring_and_deprecators(func)
    def wrapper_func(new, kwo=None):
        pass

    wrapper_func(None)
    wrapper_func(new=None)
    wrapper_func(None, kwo=None)
    wrapper_func(new=None, kwo=None)
    assert not recwarn
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        wrapper_func(old=None)
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        wrapper_func(None, None)

