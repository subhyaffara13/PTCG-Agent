
def build_expression(_, expr):  # pragma: no cover
    """Build a cupy function based on ``arrays`` and ``expr``."""

    def cupy_contract(*arrays):
        return expr._contract([to_cupy(x) for x in arrays], backend="cupy").get()

    return cupy_contract


def build_expression(backend, arrays, expr):
    """Build an expression, based on ``expr`` and initial arrays ``arrays``,
    that evaluates using backend ``backend``.
    """
    return CONVERT_BACKENDS[backend](arrays, expr)


def build_expression(_, expr):  # pragma: no cover
    """Build a jax function based on ``arrays`` and ``expr``."""
    jax, _ = _get_jax_and_to_jax()

    jax_expr = jax.jit(expr._contract)

    def jax_contract(*arrays):
        import numpy as np  # type: ignore

        return np.asarray(jax_expr(arrays))

    return jax_contract


def build_expression(arrays, expr):
    _, _, eager = _get_tensorflow_and_device()
    fn = build_expression_eager if eager else build_expression_graph
    return fn(arrays, expr)


def build_expression(arrays, expr):
    """Build a theano function based on ``arrays`` and ``expr``."""
    import theano

    in_vars = [to_theano(array) for array in arrays]
    out_var = expr._contract(in_vars, backend="theano")

    # don't supply constants to graph
    graph_ins = [x for x in in_vars if not isinstance(x, theano.tensor.TensorConstant)]
    graph = theano.function(graph_ins, out_var)

    def theano_contract(*arrays):
        return graph(*[x for x in arrays if not isinstance(x, theano.tensor.TensorConstant)])

    return theano_contract


def build_expression(_, expr):  # pragma: no cover
    """Build a torch function based on ``arrays`` and ``expr``."""

    def torch_contract(*arrays):
        torch_arrays = [to_torch(x) for x in arrays]
        torch_out = expr._contract(torch_arrays, backend="torch")

        if torch_out.device.type == "cpu":
            return torch_out.numpy()

        return torch_out.cpu().numpy()

    return torch_contract

