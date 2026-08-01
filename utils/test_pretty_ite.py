
def test_pretty_ITE():
    expr = ITE(x, y, z)
    assert pretty(expr) == (
        '/y    for x  \n'
        '<            \n'
        '\\z  otherwise'
        )
    assert upretty(expr) == """\
⎧y    for x  \n\
⎨            \n\
⎩z  otherwise\
"""

