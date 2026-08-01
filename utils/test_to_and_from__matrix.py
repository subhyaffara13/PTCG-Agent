
def test_to_and_from_Matrix():
    q = Quaternion(w, x, y, z)
    q_full = Quaternion.from_Matrix(q.to_Matrix())
    q_vect = Quaternion.from_Matrix(q.to_Matrix(True))
    assert (q - q_full).is_zero_quaternion()
    assert (q.vector_part() - q_vect).is_zero_quaternion()

