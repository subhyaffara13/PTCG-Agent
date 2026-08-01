
def test_sympy__series__sequences__EmptySequence():
    # Need to import the instance from series not the class from
    # series.sequence
    from sympy.series import EmptySequence
    assert _test_args(EmptySequence)

