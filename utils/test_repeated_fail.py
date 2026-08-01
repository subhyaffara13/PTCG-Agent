
def test_repeated_fail():
    inputs = ['1[1]', '.1e1[1]', '0x1[1]', '1.1j[1]', '1.1[1 + 1]',
        '0.1[[1]]', '0x1.1[1]']


    # All are valid Python, so only raise TypeError for invalid indexing
    for text in inputs:
        raises(TypeError, lambda: parse_expr(text))


    inputs = ['0.1[', '0.1[1', '0.1[]']
    for text in inputs:
        raises((TokenError, SyntaxError), lambda: parse_expr(text))

