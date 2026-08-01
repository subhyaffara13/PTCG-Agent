
def test_rcode_For():
    f = For(x, Range(0, 10, 2), [aug_assign(y, '*', x)])
    sol = rcode(f)
    assert sol == ("for(x in seq(from=0, to=9, by=2){\n"
                   "   y *= x;\n"
                   "}")

