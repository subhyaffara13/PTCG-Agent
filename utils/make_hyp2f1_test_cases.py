
def make_hyp2f1_test_cases(rows):
    """Generate string for a list of test cases for test_hyp2f1.py.

    Parameters
    ----------
    rows : list
        List of lists of the form [a, b, c, z, rtol] where a, b, c, z are
        parameters and the argument for hyp2f1 and rtol is an expected
        relative error for the associated test case.

    Returns
    -------
    str
        String for a list of test cases. The output string can be printed
        or saved to a file and then copied into an argument for
        `pytest.mark.parameterize` within `scipy.special.tests.test_hyp2f1.py`.
    """
    result = "[\n"
    result += '\n'.join(
        _make_hyp2f1_test_case(a, b, c, z, rtol)
        for a, b, c, z, rtol in rows
    )
    result += "\n]"
    return result

