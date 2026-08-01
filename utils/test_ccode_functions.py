
def test_ccode_functions():
    assert ccode(sin(x) ** cos(x)) == "pow(sin(x), cos(x))"

