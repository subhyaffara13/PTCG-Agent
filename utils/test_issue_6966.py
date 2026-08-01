
def test_issue_6966():
    i, k, m = symbols('i k m', integer=True)
    z_i, q_i = symbols('z_i q_i')
    a_k = Sum(-q_i*z_i/k,(i,1,m))
    b_k = a_k.diff(z_i)
    assert isinstance(b_k, Sum)
    assert b_k == Sum(-q_i/k,(i,1,m))

