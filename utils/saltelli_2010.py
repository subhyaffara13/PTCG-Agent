
def saltelli_2010(
    f_A: np.ndarray, f_B: np.ndarray, f_AB: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    r"""Saltelli2010 formulation.

    .. math::

        S_i = \frac{1}{N} \sum_{j=1}^N
        f(\mathbf{B})_j (f(\mathbf{AB}^{(i)})_j - f(\mathbf{A})_j)

    .. math::

        S_{T_i} = \frac{1}{N} \sum_{j=1}^N
        (f(\mathbf{A})_j - f(\mathbf{AB}^{(i)})_j)^2

    Parameters
    ----------
    f_A, f_B : array_like (s, n)
        Function values at A and B, respectively
    f_AB : array_like (d, s, n)
        Function values at each of the AB pages

    Returns
    -------
    s, st : array_like (s, d)
        First order and total order Sobol' indices.

    References
    ----------
    .. [1] Saltelli, A., P. Annoni, I. Azzini, F. Campolongo, M. Ratto, and
       S. Tarantola. "Variance based sensitivity analysis of model
       output. Design and estimator for the total sensitivity index."
       Computer Physics Communications, 181(2):259-270,
       :doi:`10.1016/j.cpc.2009.09.018`, 2010.
    """
    # Empirical variance calculated using output from A and B which are
    # independent. Output of AB is not independent and cannot be used
    var = np.var([f_A, f_B], axis=(0, -1))

    # We divide by the variance to have a ratio of variance
    # this leads to eq. 2
    s = np.mean(f_B * (f_AB - f_A), axis=-1) / var  # Table 2 (b)
    st = 0.5 * np.mean((f_A - f_AB) ** 2, axis=-1) / var  # Table 2 (f)

    return s.T, st.T

