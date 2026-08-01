
def test_codegen_einsum():
    if not np:
        skip("NumPy not installed")

    M = MatrixSymbol("M", 2, 2)
    N = MatrixSymbol("N", 2, 2)

    cg = convert_matrix_to_array(M * N)
    f = lambdify((M, N), cg, 'numpy')

    ma = np.array([[1, 2], [3, 4]])
    mb = np.array([[1,-2], [-1, 3]])
    assert (f(ma, mb) == np.matmul(ma, mb)).all()


def test_codegen_einsum():
    if not tf:
        skip("TensorFlow not installed")

    graph = tf.Graph()
    with graph.as_default():
        session = tf.compat.v1.Session(graph=graph)

        M = MatrixSymbol("M", 2, 2)
        N = MatrixSymbol("N", 2, 2)

        cg = convert_matrix_to_array(M * N)
        f = lambdify((M, N), cg, 'tensorflow')

        ma = tf.constant([[1, 2], [3, 4]])
        mb = tf.constant([[1,-2], [-1, 3]])
        y = session.run(f(ma, mb))
        c = session.run(tf.matmul(ma, mb))
        assert (y == c).all()

