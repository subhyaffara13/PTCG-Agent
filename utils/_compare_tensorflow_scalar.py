
def _compare_tensorflow_scalar(
    variables, expr, rng=lambda: random.randint(0, 10)):
    f = lambdify(variables, expr, 'tensorflow')
    rvs = [rng() for v in variables]

    graph = tf.Graph()
    r = None
    with graph.as_default():
        tf_rvs = [eval(tensorflow_code(i)) for i in rvs]
        session = tf.compat.v1.Session(graph=graph)
        r = session.run(f(*tf_rvs))

    e = expr.subs(dict(zip(variables, rvs))).evalf().doit()
    assert abs(r-e) < 10**-6

