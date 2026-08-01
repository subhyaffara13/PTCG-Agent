
def test_ccode_For():
    f = For(x, Range(0, 10, 2), [aug_assign(y, '*', x)])
    assert ccode(f) == ("for (x = 0; x < 10; x += 2) {\n"
                        "   y *= x;\n"
                        "}")

