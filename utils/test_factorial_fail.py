
def test_factorial_fail():
    inputs = ['x!!!', 'x!!!!', '(!)']


    for text in inputs:
        try:
            parse_expr(text)
            assert False
        except TokenError:
            assert True

