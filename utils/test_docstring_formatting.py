
def test_docstring_formatting():
    docstr = dedent(
        """
        This is the cumsum method.

        It computes the cumulative sum.
        """
    )
    assert cumsum.__doc__ == docstr

