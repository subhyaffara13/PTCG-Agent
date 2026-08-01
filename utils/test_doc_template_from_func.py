
def test_doc_template_from_func():
    docstr = dedent(
        """
        This is the cummax method.

        It computes the cumulative maximum.
        """
    )
    assert cummax.__doc__ == docstr

