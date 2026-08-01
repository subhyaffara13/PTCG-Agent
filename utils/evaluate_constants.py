
def evaluate_constants(const_arrays, expr):  # pragma: no cover
    """Convert constant arguments to cupy arrays, and perform any possible
    constant contractions.
    """
    return expr(*[to_cupy(x) for x in const_arrays], backend="cupy", evaluate_constants=True)


def evaluate_constants(backend, arrays, expr):
    """Convert constant arrays to the correct backend, and perform as much of
    the contraction of ``expr`` with these as possible.
    """
    return EVAL_CONSTS_BACKENDS[backend](arrays, expr)


def evaluate_constants(const_arrays, expr):  # pragma: no cover
    """Convert constant arguments to jax arrays, and perform any possible
    constant contractions.
    """
    jax, to_jax = _get_jax_and_to_jax()

    return expr(*[to_jax(x) for x in const_arrays], backend="jax", evaluate_constants=True)


def evaluate_constants(const_arrays, expr):
    _, _, eager = _get_tensorflow_and_device()
    fn = evaluate_constants_eager if eager else evaluate_constants_graph
    return fn(const_arrays, expr)


def evaluate_constants(const_arrays, expr):
    # compute the partial graph of new inputs
    const_arrays = [to_theano(x, constant=True) for x in const_arrays]
    new_ops, new_contraction_list = expr(*const_arrays, backend="theano", evaluate_constants=True)

    # evaluate the new inputs and convert to theano shared tensors
    new_ops = [None if x is None else to_theano(x.eval(), constant=True) for x in new_ops]

    return new_ops, new_contraction_list


def evaluate_constants(const_arrays, expr):
    """Convert constant arguments to torch, and perform any possible constant
    contractions.
    """
    const_arrays = [to_torch(x) for x in const_arrays]
    return expr(*const_arrays, backend="torch", evaluate_constants=True)

