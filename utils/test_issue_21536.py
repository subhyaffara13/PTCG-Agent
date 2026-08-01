
def test_issue_21536():
    #test to check evaluate=False in case of iterable input
    u = sympify("x+3*x+2", evaluate=False)
    v = sympify("2*x+4*x+2+4", evaluate=False)

    assert u.is_Add and set(u.args) == {x, 3*x, 2}
    assert v.is_Add and set(v.args) == {2*x, 4*x, 2, 4}
    assert sympify(["x+3*x+2", "2*x+4*x+2+4"], evaluate=False) == [u, v]

    #test to check evaluate=True in case of iterable input
    u = sympify("x+3*x+2", evaluate=True)
    v = sympify("2*x+4*x+2+4", evaluate=True)

    assert u.is_Add and set(u.args) == {4*x, 2}
    assert v.is_Add and set(v.args) == {6*x, 6}
    assert sympify(["x+3*x+2", "2*x+4*x+2+4"], evaluate=True) == [u, v]

    #test to check evaluate with no input in case of iterable input
    u = sympify("x+3*x+2")
    v = sympify("2*x+4*x+2+4")

    assert u.is_Add and set(u.args) == {4*x, 2}
    assert v.is_Add and set(v.args) == {6*x, 6}
    assert sympify(["x+3*x+2", "2*x+4*x+2+4"]) == [u, v]

