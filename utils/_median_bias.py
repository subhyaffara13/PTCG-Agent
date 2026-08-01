
def _median_bias(n):
    """
    Returns the bias of the median of a set of periodograms relative to
    the mean.

    See Appendix B from [1]_ for details.

    Parameters
    ----------
    n : int
        Numbers of periodograms being averaged.

    Returns
    -------
    bias : float
        Calculated bias.

    References
    ----------
    .. [1] B. Allen, W.G. Anderson, P.R. Brady, D.A. Brown, J.D.E. Creighton.
           "FINDCHIRP: an algorithm for detection of gravitational waves from
           inspiraling compact binaries", Physical Review D 85, 2012,
           :arxiv:`gr-qc/0509116`
    """
    ii_2 = 2 * np.arange(1., (n-1) // 2 + 1)
    return 1 + np.sum(1. / (ii_2 + 1) - 1. / ii_2)


def _median_bias(n: int) -> Array:
  """
  Returns the bias of the median of a set of periodograms relative to
  the mean. See Appendix B from [1]_ for details.

  Args:
   n : int
      Numbers of periodograms being averaged.

  Returns:
    bias : float
      Calculated bias.

  References:
  .. [1] B. Allen, W.G. Anderson, P.R. Brady, D.A. Brown, J.D.E. Creighton.
          "FINDCHIRP: an algorithm for detection of gravitational waves from
          inspiraling compact binaries", Physical Review D 85, 2012,
          :arxiv:`gr-qc/0509116`
  """
  ii_2 = jnp.arange(2., n, 2)
  return 1 + jnp.sum(1. / (ii_2 + 1) - 1. / ii_2)

