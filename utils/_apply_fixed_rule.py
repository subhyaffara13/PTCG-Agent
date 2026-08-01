
def _apply_fixed_rule(f, a, b, orig_nodes, orig_weights, args, xp):
    # Downcast nodes and weights to common dtype of a and b
    result_dtype = a.dtype
    orig_nodes = xp.astype(orig_nodes, result_dtype)
    orig_weights = xp.astype(orig_weights, result_dtype)

    # Ensure orig_nodes are at least 2D, since 1D cubature methods can return arrays of
    # shape (npoints,) rather than (npoints, 1)
    if orig_nodes.ndim == 1:
        orig_nodes = orig_nodes[:, None]

    rule_ndim = orig_nodes.shape[-1]

    a_ndim = xp_size(a)
    b_ndim = xp_size(b)

    if rule_ndim != a_ndim or rule_ndim != b_ndim:
        raise ValueError(f"rule and function are of incompatible dimension, nodes have"
                         f"ndim {rule_ndim}, while limit of integration has ndim"
                         f"a_ndim={a_ndim}, b_ndim={b_ndim}")

    lengths = b - a

    # The underlying rule is for the hypercube [-1, 1]^n.
    #
    # To handle arbitrary regions of integration, it's necessary to apply a linear
    # change of coordinates to map each interval [a[i], b[i]] to [-1, 1].
    nodes = (orig_nodes + 1) * (lengths * 0.5) + a

    # Also need to multiply the weights by a scale factor equal to the determinant
    # of the Jacobian for this coordinate change.
    weight_scale_factor = xp.prod(lengths, dtype=result_dtype) / 2**rule_ndim
    weights = orig_weights * weight_scale_factor

    f_nodes = f(nodes, *args)
    weights_reshaped = xp.reshape(weights, (-1, *([1] * (f_nodes.ndim - 1))))

    # f(nodes) will have shape (num_nodes, output_dim_1, ..., output_dim_n)
    # Summing along the first axis means estimate will shape (output_dim_1, ...,
    # output_dim_n)
    est = xp.sum(weights_reshaped * f_nodes, axis=0, dtype=result_dtype)

    return est

