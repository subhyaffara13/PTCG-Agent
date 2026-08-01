
def _compare_tensorflow_matrix_scalar(variables, expr):
    f = lambdify(variables, expr, 'tensorflow')
    random_matrices = [
        randMatrix(v.rows, v.cols).evalf() / 100 for v in variables]

    graph = tf.Graph()
    r = None
    with graph.as_default():
        random_variables = [eval(tensorflow_code(i)) for i in random_matrices]
        session = tf.compat.v1.Session(graph=graph)
        r = session.run(f(*random_variables))

    e = expr.subs(dict(zip(variables, random_matrices)))
    e = e.doit()
    assert abs(r-e) < 10**-6

