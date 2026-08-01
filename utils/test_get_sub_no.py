
def test_get_subNO():
    p, q, r = symbols('p,q,r')
    assert NO(F(p)*F(q)*F(r)).get_subNO(1) == NO(F(p)*F(r))
    assert NO(F(p)*F(q)*F(r)).get_subNO(0) == NO(F(q)*F(r))
    assert NO(F(p)*F(q)*F(r)).get_subNO(2) == NO(F(p)*F(q))

