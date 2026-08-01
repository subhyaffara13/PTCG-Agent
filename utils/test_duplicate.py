
def test_duplicate():
    from sympy.core.function import BadSignatureError
    # test coverage for line 95 in conditionset.py, check for duplicates in symbols
    dup = symbols('a,a')
    raises(BadSignatureError, lambda: ConditionSet(dup, x < 0))

