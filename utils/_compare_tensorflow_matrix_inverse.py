
def _compare_tensorflow_matrix_inverse(variables, expr, use_float=False):
    f = lambdify(variables, expr, 'tensorflow')
    if not use_float:
        random_matrices = [eye(v.rows, v.cols)*4 for v in variables]
    else:
        random_matrices = [eye(v.rows, v.cols)*3.14 for v in variables]

    graph = tf.Graph()
    r = None
    with graph.as_default():
        random_variables = [eval(tensorflow_code(i)) for i in random_matrices]
        session = tf.compat.v1.Session(graph=graph)
        r = session.run(f(*random_variables))

    e = expr.subs(dict(zip(variables, random_matrices)))
    e = e.doit()
    if e.is_Matrix:
        if not isinstance(e, MatrixBase):
            e = e.as_explicit()
        e = e.tolist()

    if not use_float:
        assert (r == e).all()
    else:
        r = [i for row in r for i in row]
        e = [i for row in e for i in row]
        assert all(
            abs(a-b) < 10**-(4-int(log(abs(a), 10))) for a, b in zip(r, e))

