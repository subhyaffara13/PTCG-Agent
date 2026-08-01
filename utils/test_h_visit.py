
def test_h_visit(code, expected):
    code = dedent(code)
    # test for almost-equality
    for act, exp in zip(h_visit(code), expected):
        for a, e in zip(act, exp):
            assert a == e or int(a * 10 ** 3) == int(e * 10 ** 3)

