
def test_vector_outer():
    a, b, c, d, e, f = symbols('a, b, c, d, e, f')
    N = ReferenceFrame('N')
    v1 = a*N.x + b*N.y + c*N.z
    v2 = d*N.x + e*N.y + f*N.z
    v1v2 = Matrix([[a*d, a*e, a*f],
                   [b*d, b*e, b*f],
                   [c*d, c*e, c*f]])
    assert v1.outer(v2).to_matrix(N) == v1v2
    assert (v1 | v2).to_matrix(N) == v1v2
    v2v1 = Matrix([[d*a, d*b, d*c],
                   [e*a, e*b, e*c],
                   [f*a, f*b, f*c]])
    assert v2.outer(v1).to_matrix(N) == v2v1
    assert (v2 | v1).to_matrix(N) == v2v1

