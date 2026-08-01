
def test_trigsimp():
    assert trigsimp(A*sin(x)**2 + A*cos(x)**2) == A


def test_trigsimp():
    # issue 16736
    s, c = sin(2*x), cos(2*x)
    eq = Eq(s, c)
    assert trigsimp(eq) == eq  # no rearrangement of sides
    # simplification of sides might result in
    # an unevaluated Eq
    changed = trigsimp(Eq(s + c, sqrt(2)))
    assert isinstance(changed, Eq)
    assert changed.subs(x, pi/8) is S.true
    # or an evaluated one
    assert trigsimp(Eq(cos(x)**2 + sin(x)**2, 1)) is S.true

