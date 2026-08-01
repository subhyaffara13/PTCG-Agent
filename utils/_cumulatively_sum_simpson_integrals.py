
def _cumulatively_sum_simpson_integrals(
    y: np.ndarray,
    dx: np.ndarray,
    integration_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    xp
) -> np.ndarray:
    """Calculate cumulative sum of Simpson integrals.
    Takes as input the integration function to be used.
    The integration_func is assumed to return the cumulative sum using
    composite Simpson's rule. Assumes the axis of summation is -1.
    """
    sub_integrals_h1 = integration_func(y, dx)
    sub_integrals_h2 = xp.flip(
        integration_func(xp.flip(y, axis=-1), xp.flip(dx, axis=-1)),
        axis=-1
    )

    shape = list(sub_integrals_h1.shape)
    shape[-1] += 1
    sub_integrals = xp.empty(shape, dtype=xp.result_type(y, dx))
    sub_integrals[..., :-1:2] = sub_integrals_h1[..., ::2]
    sub_integrals[..., 1::2] = sub_integrals_h2[..., ::2]
    # Integral over last subinterval can only be calculated from
    # formula for h2
    sub_integrals[..., -1] = sub_integrals_h2[..., -1]
    res = xp.cumulative_sum(sub_integrals, axis=-1)
    return res

