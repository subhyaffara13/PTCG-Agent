
def test_element_like_objects():
    len_y = 5
    y = ArraySymbol('y', shape=(len_y,))
    x = ArraySymbol('x', shape=(len_y,))
    Dy = ArraySymbol('Dy', shape=(len_y-1,))
    i = Idx('i', len_y-1)
    e=Eq(Dy[i], (y[i+1]-y[i])/(x[i+1]-x[i]))
    code0 = fcode(Assignment(e.lhs, e.rhs))
    assert code0.endswith('Dy(i) = (y(i + 1) - y(i))/(x(i + 1) - x(i))')

    class ElementExpr(Element, Expr):
        pass

    e = e.subs((a, ElementExpr(a.name, a.indices)) for a in e.atoms(ArrayElement)  )
    e=Eq(Dy[i], (y[i+1]-y[i])/(x[i+1]-x[i]))
    code0 = fcode(Assignment(e.lhs, e.rhs))
    assert code0.endswith('Dy(i) = (y(i + 1) - y(i))/(x(i + 1) - x(i))')

