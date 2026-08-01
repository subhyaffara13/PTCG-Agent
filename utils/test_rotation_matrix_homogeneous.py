
def test_rotation_matrix_homogeneous():
    q = Quaternion(w, x, y, z)
    R1 = q.to_rotation_matrix(homogeneous=True) * q.norm()**2
    R2 = simplify(q.to_rotation_matrix(homogeneous=False) * q.norm()**2)
    assert R1 == R2

