
def test_var():
    ns = {"var": var, "raises": raises}
    eval("var('a')", ns)
    assert ns["a"] == Symbol("a")

    eval("var('b bb cc zz _x')", ns)
    assert ns["b"] == Symbol("b")
    assert ns["bb"] == Symbol("bb")
    assert ns["cc"] == Symbol("cc")
    assert ns["zz"] == Symbol("zz")
    assert ns["_x"] == Symbol("_x")

    v = eval("var(['d', 'e', 'fg'])", ns)
    assert ns['d'] == Symbol('d')
    assert ns['e'] == Symbol('e')
    assert ns['fg'] == Symbol('fg')

# check return value
    assert v != ['d', 'e', 'fg']
    assert v == [Symbol('d'), Symbol('e'), Symbol('fg')]

