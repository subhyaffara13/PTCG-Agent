
def test_endianness():
    d = np.ones((3,4))
    offsets = [-1,0,1]

    a = dia_matrix((d.astype('<f8'), offsets), (4, 4))
    b = dia_matrix((d.astype('>f8'), offsets), (4, 4))
    v = np.arange(4)

    assert_allclose(a.dot(v), [1, 3, 6, 5])
    assert_allclose(b.dot(v), [1, 3, 6, 5])

