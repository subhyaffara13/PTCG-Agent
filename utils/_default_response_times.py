
def _default_response_times(A, n):
    """Compute a reasonable set of time samples for the response time.

    This function is used by `impulse` and `step`  to compute the response time
    when the `T` argument to the function is None.

    Parameters
    ----------
    A : array_like
        The system matrix, which is square.
    n : int
        The number of time samples to generate.

    Returns
    -------
    t : ndarray
        The 1-D array of length `n` of time samples at which the response
        is to be computed.
    """
    # Create a reasonable time interval.
    # TODO: This could use some more work.
    # For example, what is expected when the system is unstable?
    vals = linalg.eigvals(A)
    r = min(abs(real(vals)))
    if r == 0.0:
        r = 1.0
    tc = 1.0 / r
    t = linspace(0.0, 7 * tc, n)
    return t

