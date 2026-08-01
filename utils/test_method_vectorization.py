
def test_method_vectorization():
    o = m.VectorizeTestClass(3)
    x = np.array([1, 2], dtype="int")
    y = np.array([[10], [20]], dtype="float32")
    assert np.all(o.method(x, y) == [[14, 15], [24, 25]])

