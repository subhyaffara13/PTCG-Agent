
def _lnB(alpha):
    r"""Internal helper function to compute the log of the useful quotient.

    .. math::

        B(\alpha) = \frac{\prod_{i=1}{K}\Gamma(\alpha_i)}
                         {\Gamma\left(\sum_{i=1}^{K} \alpha_i \right)}

    Parameters
    ----------
    %(_dirichlet_doc_default_callparams)s

    Returns
    -------
    B : scalar
        Helper quotient, internal use only

    """
    return np.sum(gammaln(alpha)) - gammaln(np.sum(alpha))

