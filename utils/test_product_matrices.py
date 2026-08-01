
def test_product_matrices():
    q1 = Quaternion(w, x, y, z)
    q2 = Quaternion(*(symbols("a:d")))
    assert (q1 * q2).to_Matrix() == q1.product_matrix_left * q2.to_Matrix()
    assert (q1 * q2).to_Matrix() == q2.product_matrix_right * q1.to_Matrix()

    R1 = (q1.product_matrix_left * q1.product_matrix_right.T)[1:, 1:]
    R2 = simplify(q1.to_rotation_matrix()*q1.norm()**2)
    assert R1 == R2

