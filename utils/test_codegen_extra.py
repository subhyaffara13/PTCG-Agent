
def test_codegen_extra():
    if not np:
        skip("NumPy not installed")

    M = MatrixSymbol("M", 2, 2)
    N = MatrixSymbol("N", 2, 2)
    P = MatrixSymbol("P", 2, 2)
    Q = MatrixSymbol("Q", 2, 2)
    ma = np.array([[1, 2], [3, 4]])
    mb = np.array([[1,-2], [-1, 3]])
    mc = np.array([[2, 0], [1, 2]])
    md = np.array([[1,-1], [4, 7]])

    cg = ArrayTensorProduct(M, N)
    f = lambdify((M, N), cg, 'numpy')
    assert (f(ma, mb) == np.einsum(ma, [0, 1], mb, [2, 3])).all()

    cg = ArrayAdd(M, N)
    f = lambdify((M, N), cg, 'numpy')
    assert (f(ma, mb) == ma+mb).all()

    cg = ArrayAdd(M, N, P)
    f = lambdify((M, N, P), cg, 'numpy')
    assert (f(ma, mb, mc) == ma+mb+mc).all()

    cg = ArrayAdd(M, N, P, Q)
    f = lambdify((M, N, P, Q), cg, 'numpy')
    assert (f(ma, mb, mc, md) == ma+mb+mc+md).all()

    cg = PermuteDims(M, [1, 0])
    f = lambdify((M,), cg, 'numpy')
    assert (f(ma) == ma.T).all()

    cg = PermuteDims(ArrayTensorProduct(M, N), [1, 2, 3, 0])
    f = lambdify((M, N), cg, 'numpy')
    assert (f(ma, mb) == np.transpose(np.einsum(ma, [0, 1], mb, [2, 3]), (1, 2, 3, 0))).all()

    cg = ArrayDiagonal(ArrayTensorProduct(M, N), (1, 2))
    f = lambdify((M, N), cg, 'numpy')
    assert (f(ma, mb) == np.diagonal(np.einsum(ma, [0, 1], mb, [2, 3]), axis1=1, axis2=2)).all()


def test_codegen_extra():
    if not tf:
        skip("TensorFlow not installed")

    graph = tf.Graph()
    with graph.as_default():
        session = tf.compat.v1.Session()

        M = MatrixSymbol("M", 2, 2)
        N = MatrixSymbol("N", 2, 2)
        P = MatrixSymbol("P", 2, 2)
        Q = MatrixSymbol("Q", 2, 2)
        ma = tf.constant([[1, 2], [3, 4]])
        mb = tf.constant([[1,-2], [-1, 3]])
        mc = tf.constant([[2, 0], [1, 2]])
        md = tf.constant([[1,-1], [4, 7]])

        cg = ArrayTensorProduct(M, N)
        assert tensorflow_code(cg) == \
            'tensorflow.linalg.einsum("ab,cd", M, N)'
        f = lambdify((M, N), cg, 'tensorflow')
        y = session.run(f(ma, mb))
        c = session.run(tf.einsum("ij,kl", ma, mb))
        assert (y == c).all()

        cg = ArrayAdd(M, N)
        assert tensorflow_code(cg) == 'tensorflow.math.add(M, N)'
        f = lambdify((M, N), cg, 'tensorflow')
        y = session.run(f(ma, mb))
        c = session.run(ma + mb)
        assert (y == c).all()

        cg = ArrayAdd(M, N, P)
        assert tensorflow_code(cg) == \
            'tensorflow.math.add(tensorflow.math.add(M, N), P)'
        f = lambdify((M, N, P), cg, 'tensorflow')
        y = session.run(f(ma, mb, mc))
        c = session.run(ma + mb + mc)
        assert (y == c).all()

        cg = ArrayAdd(M, N, P, Q)
        assert tensorflow_code(cg) == \
            'tensorflow.math.add(' \
                'tensorflow.math.add(tensorflow.math.add(M, N), P), Q)'
        f = lambdify((M, N, P, Q), cg, 'tensorflow')
        y = session.run(f(ma, mb, mc, md))
        c = session.run(ma + mb + mc + md)
        assert (y == c).all()

        cg = PermuteDims(M, [1, 0])
        assert tensorflow_code(cg) == 'tensorflow.transpose(M, [1, 0])'
        f = lambdify((M,), cg, 'tensorflow')
        y = session.run(f(ma))
        c = session.run(tf.transpose(ma))
        assert (y == c).all()

        cg = PermuteDims(ArrayTensorProduct(M, N), [1, 2, 3, 0])
        assert tensorflow_code(cg) == \
            'tensorflow.transpose(' \
                'tensorflow.linalg.einsum("ab,cd", M, N), [1, 2, 3, 0])'
        f = lambdify((M, N), cg, 'tensorflow')
        y = session.run(f(ma, mb))
        c = session.run(tf.transpose(tf.einsum("ab,cd", ma, mb), [1, 2, 3, 0]))
        assert (y == c).all()

        cg = ArrayDiagonal(ArrayTensorProduct(M, N), (1, 2))
        assert tensorflow_code(cg) == \
            'tensorflow.linalg.einsum("ab,bc->acb", M, N)'
        f = lambdify((M, N), cg, 'tensorflow')
        y = session.run(f(ma, mb))
        c = session.run(tf.einsum("ab,bc->acb", ma, mb))
        assert (y == c).all()

