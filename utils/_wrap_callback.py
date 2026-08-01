
def _wrap_callback(callback, method=None):
    """Wrap a user-provided callback so that attributes can be attached."""
    if callback is None or method in {'tnc', 'cobyla', 'cobyqa'}:
        return callback  # don't wrap

    sig = wrapped_inspect_signature(callback)

    if set(sig.parameters) == {'intermediate_result'}:
        def wrapped_callback(res):
            return callback(intermediate_result=res)
    elif method == 'trust-constr':
        def wrapped_callback(res):
            return callback(np.copy(res.x), res)
    elif method == 'differential_evolution':
        def wrapped_callback(res):
            return callback(np.copy(res.x), res.convergence)
    else:
        def wrapped_callback(res):
            return callback(np.copy(res.x))

    wrapped_callback.stop_iteration = False
    return wrapped_callback

