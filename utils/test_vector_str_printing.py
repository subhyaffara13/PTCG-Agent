
def test_vector_str_printing():
    assert vsprint(w) == 'alpha*N.x + sin(omega)*N.y + alpha*beta*N.z'
    assert vsprint(omega.diff() * N.x) == "omega'*N.x"
    assert vsstrrepr(w) == 'alpha*N.x + sin(omega)*N.y + alpha*beta*N.z'

