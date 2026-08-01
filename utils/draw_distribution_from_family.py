
def draw_distribution_from_family(family, data, rng, proportions, min_side=0):
    # If the distribution has parameters, choose a parameterization and
    # draw broadcastable shapes for the parameter arrays.
    n_parameterizations = family._num_parameterizations()
    if n_parameterizations > 0:
        i = data.draw(strategies.integers(0, max_value=n_parameterizations-1))
        n_parameters = family._num_parameters(i)
        shapes, result_shape = data.draw(
            npst.mutually_broadcastable_shapes(num_shapes=n_parameters,
                                               min_side=min_side))
        dist = family._draw(shapes, rng=rng, proportions=proportions,
                            i_parameterization=i)
    else:
        dist = family._draw(rng=rng)
        result_shape = tuple()

    # Draw a broadcastable shape for the arguments, and draw values for the
    # arguments.
    x_shape = data.draw(npst.broadcastable_shapes(result_shape,
                                                  min_side=min_side))
    x = dist._variable.draw(x_shape, parameter_values=dist._parameters,
                            proportions=proportions, rng=rng, region='typical')
    x_result_shape = np.broadcast_shapes(x_shape, result_shape)
    y_shape = data.draw(npst.broadcastable_shapes(x_result_shape,
                                                  min_side=min_side))
    y = dist._variable.draw(y_shape, parameter_values=dist._parameters,
                            proportions=proportions, rng=rng, region='typical')
    xy_result_shape = np.broadcast_shapes(y_shape, x_result_shape)
    p_domain = _RealInterval((0, 1), (True, True))
    p_var = _RealParameter('p', domain=p_domain)
    p = p_var.draw(x_shape, proportions=proportions, rng=rng)
    with np.errstate(divide='ignore', invalid='ignore'):
        logp = np.log(p)

    return dist, x, y, p, logp, result_shape, x_result_shape, xy_result_shape

