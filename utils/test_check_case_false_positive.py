
def test_check_case_false_positive():
    # The upper case/lower case exception should not be triggered by SymPy
    # objects that differ only because of assumptions.  (It may be useful to
    # have a check for that as well, but here we only want to test against
    # false positives with respect to case checking.)
    x1 = symbols('x')
    x2 = symbols('x', my_assumption=True)
    try:
        codegen(('test', x1*x2), 'f95', 'prefix')
    except CodeGenError as e:
        if e.args[0].startswith("Fortran ignores case."):
            raise AssertionError("This exception should not be raised!")

