
def test_vector_str_arguments():
    assert vsprint(N.x * 3.0, full_prec=False) == '3.0*N.x'
    assert vsprint(N.x * 3.0, full_prec=True) == '3.00000000000000*N.x'

