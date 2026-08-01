
def test_issue_9538():
    eq = x - 3*y + 2
    assert diophantine(eq, syms=[y,x]) == {(t_0, 3*t_0 - 2)}
    raises(TypeError, lambda: diophantine(eq, syms={y, x}))

