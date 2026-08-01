
def _log_gauss_mass(a, b):
    """Log of Gaussian probability mass within an interval"""
    a, b = np.broadcast_arrays(a, b)

    # Calculations in right tail are inaccurate, so we'll exploit the
    # symmetry and work only in the left tail
    case_left = b <= 0
    case_right = a > 0
    case_central = ~(case_left | case_right)

    def mass_case_left(a, b):
        return _log_diff(_norm_logcdf(b), _norm_logcdf(a))

    def mass_case_right(a, b):
        return mass_case_left(-b, -a)

    def mass_case_central(a, b):
        # Previously, this was implemented as:
        # left_mass = mass_case_left(a, 0)
        # right_mass = mass_case_right(0, b)
        # return _log_sum(left_mass, right_mass)
        # Catastrophic cancellation occurs as np.exp(log_mass) approaches 1.
        # Correct for this with an alternative formulation.
        # We're not concerned with underflow here: if only one term
        # underflows, it was insignificant; if both terms underflow,
        # the result can't accurately be represented in logspace anyway
        # because sc.log1p(x) ~ x for small x.
        return sc.log1p(-_norm_cdf(a) - _norm_cdf(-b))

    # _lazyselect not working; don't care to debug it
    out = np.full_like(a, fill_value=np.nan, dtype=np.complex128)
    if a[case_left].size:
        out[case_left] = mass_case_left(a[case_left], b[case_left])
    if a[case_right].size:
        out[case_right] = mass_case_right(a[case_right], b[case_right])
    if a[case_central].size:
        out[case_central] = mass_case_central(a[case_central], b[case_central])
    return np.real(out)  # discard ~0j


def _log_gauss_mass(a, b):
  """Log of Gaussian probability mass within an interval"""
  a, b = jnp.array(a), jnp.array(b)
  a, b = jnp.broadcast_arrays(a, b)

  # Note: Docstring carried over from scipy
  # Calculations in right tail are inaccurate, so we'll exploit the
  # symmetry and work only in the left tail
  case_left = b <= 0
  case_right = a > 0
  case_central = ~(case_left | case_right)

  # By conditionally swapping arguments if we're in the right tail,
  # we only need to compile the mass_case_left graph once instead of twice.
  a_tail = jnp.where(case_right, -b, a)
  b_tail = jnp.where(case_right, -a, b)

  mass_tail = _log_diff(log_ndtr(b_tail), log_ndtr(a_tail))

  # Catastrophic cancellation occurs as np.exp(log_mass) approaches 1.
  # Correct for this with an alternative formulation.
  # We're not concerned with underflow here: if only one term
  # underflows, it was insignificant; if both terms underflow,
  # the result can't accurately be represented in logspace anyway
  # because sc.log1p(x) ~ x for small x.
  mass_central = jnp.log1p(-ndtr(a) - ndtr(-b))

  out = jnp.where(case_central, mass_central, mass_tail)
  return out

