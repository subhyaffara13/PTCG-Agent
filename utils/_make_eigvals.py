
def _make_eigvals(alpha, beta, homogeneous_eigvals):
    if homogeneous_eigvals:
        if beta is None:
            beta = np.ones_like(alpha)
        return np.stack((alpha, beta), axis=-2)
    else:
        if beta is None:
            return alpha
        else:
            w = np.empty_like(alpha)
            alpha_zero = (alpha == 0)
            beta_zero = (beta == 0)
            beta_nonzero = ~beta_zero
            w[beta_nonzero] = alpha[beta_nonzero] / beta[beta_nonzero]
            # Use np.inf for complex values too since
            # 1/np.inf = 0, i.e., it correctly behaves as projective
            # infinity.
            w[~alpha_zero & beta_zero] = np.inf
            if np.all(alpha.imag == 0):
                w[alpha_zero & beta_zero] = np.nan
            else:
                w[alpha_zero & beta_zero] = complex(np.nan, np.nan)
            return w

