
def test_struct():
    vx, vy = Variable(x, type=float64), Variable(y, type=float64)
    s = struct('vec2', [vx, vy])
    assert s.func(*s.args) == s
    assert s == struct('vec2', (vx, vy))
    assert s != struct('vec2', (vy, vx))
    assert str(s.name) == 'vec2'
    assert len(s.declarations) == 2
    assert all(isinstance(arg, Declaration) for arg in s.declarations)
    assert ccode(s) == (
        "struct vec2 {\n"
        "   double x;\n"
        "   double y;\n"
        "}")

