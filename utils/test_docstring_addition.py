
def test_docstring_addition():
    @_preprocess_data()
    def funcy(ax, *args, **kwargs):
        """
        Parameters
        ----------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER
        """

    assert re.search(r"all parameters also accept a string", funcy.__doc__)
    assert not re.search(r"the following parameters", funcy.__doc__)

    @_preprocess_data(replace_names=[])
    def funcy(ax, x, y, z, bar=None):
        """
        Parameters
        ----------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER
        """

    assert not re.search(r"all parameters also accept a string", funcy.__doc__)
    assert not re.search(r"the following parameters", funcy.__doc__)

    @_preprocess_data(replace_names=["bar"])
    def funcy(ax, x, y, z, bar=None):
        """
        Parameters
        ----------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER
        """

    assert not re.search(r"all parameters also accept a string", funcy.__doc__)
    assert not re.search(r"the following parameters .*: \*bar\*\.",
                         funcy.__doc__)

    @_preprocess_data(replace_names=["x", "t"])
    def funcy(ax, x, y, z, t=None):
        """
        Parameters
        ----------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER
        """

    assert not re.search(r"all parameters also accept a string", funcy.__doc__)
    assert not re.search(r"the following parameters .*: \*x\*, \*t\*\.",
                         funcy.__doc__)

