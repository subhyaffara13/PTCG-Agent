
def test_fcode_Indexed_without_looking_for_contraction():
    len_y = 5
    y = IndexedBase('y', shape=(len_y,))
    x = IndexedBase('x', shape=(len_y,))
    Dy = IndexedBase('Dy', shape=(len_y-1,))
    i = Idx('i', len_y-1)
    e=Eq(Dy[i], (y[i+1]-y[i])/(x[i+1]-x[i]))
    code0 = fcode(e.rhs, assign_to=e.lhs, contract=False)
    assert code0.endswith('Dy(i) = (y(i + 1) - y(i))/(x(i + 1) - x(i))')

