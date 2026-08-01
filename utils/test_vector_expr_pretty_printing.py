
def test_vector_expr_pretty_printing():
    A = CoordSys3D('A')

    assert upretty(Cross(A.i, A.x*A.i+3*A.y*A.j)) == "(i_A)×((x_A) i_A + (3⋅y_A) j_A)"
    assert upretty(x*Cross(A.i, A.j)) == 'x⋅(i_A)×(j_A)'

    assert upretty(Curl(A.x*A.i + 3*A.y*A.j)) == "∇×((x_A) i_A + (3⋅y_A) j_A)"

    assert upretty(Divergence(A.x*A.i + 3*A.y*A.j)) == "∇⋅((x_A) i_A + (3⋅y_A) j_A)"

    assert upretty(Dot(A.i, A.x*A.i+3*A.y*A.j)) == "(i_A)⋅((x_A) i_A + (3⋅y_A) j_A)"

    assert upretty(Gradient(A.x+3*A.y)) == "∇(x_A + 3⋅y_A)"
    assert upretty(Laplacian(A.x+3*A.y)) == "∆(x_A + 3⋅y_A)"

