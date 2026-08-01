
def test_Declaration():
    u = symbols('u', real=True)
    vu = Variable(u, type=Type.from_expr(u))
    assert Declaration(vu).variable.type == real
    vn = Variable(n, type=Type.from_expr(n))
    assert Declaration(vn).variable.type == integer

    # PR 19107, does not allow comparison between expressions and Basic
    # lt = StrictLessThan(vu, vn)
    # assert isinstance(lt, StrictLessThan)

    vuc = Variable(u, Type.from_expr(u), value=3.0, attrs={value_const})
    assert value_const in vuc.attrs
    assert pointer_const not in vuc.attrs
    decl = Declaration(vuc)
    assert decl.variable == vuc
    assert isinstance(decl.variable.value, Float)
    assert decl.variable.value == 3.0
    assert decl.func(*decl.args) == decl
    assert vuc.as_Declaration() == decl
    assert vuc.as_Declaration(value=None, attrs=None) == Declaration(vu)

    vy = Variable(y, type=integer, value=3)
    decl2 = Declaration(vy)
    assert decl2.variable == vy
    assert decl2.variable.value == Integer(3)

    vi = Variable(i, type=Type.from_expr(i), value=3.0)
    decl3 = Declaration(vi)
    assert decl3.variable.type == integer
    assert decl3.variable.value == 3.0

    raises(ValueError, lambda: Declaration(vi, 42))

