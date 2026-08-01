
def check_jvp(f, f_jvp, args, atol=None, rtol=None, eps=EPS, err_msg=''):
  """Check a JVP from automatic differentiation against finite differences.

  Gradients are only checked in a single randomly chosen direction, which
  ensures that the finite difference calculation does not become prohibitively
  expensive even for large input/output spaces.

  Args:
    f: function to check at ``f(*args)``.
    f_jvp: function that calculates ``jax.jvp`` applied to ``f``. Typically this
      should be ``functools.partial(jax.jvp, f)``.
    args: tuple of argument values.
    atol: absolute tolerance for gradient equality.
    rtol: relative tolerance for gradient equality.
    eps: step size used for finite differences.
    err_msg: additional error message to include if checks fail.

  Raises:
    AssertionError: if gradients do not match.
  """
  atol = _merge_tolerance(atol, default_gradient_tolerance)
  rtol = _merge_tolerance(rtol, default_gradient_tolerance)
  rng = np.random.RandomState(0)
  tangent = tree_map(partial(rand_like, rng), args)
  v_out, t_out = f_jvp(args, tangent)
  _check_dtypes_match(v_out, t_out)
  v_out_expected = f(*args)
  _check_dtypes_match(v_out, v_out_expected)
  t_out_expected = numerical_jvp(f, args, tangent, eps=eps)
  # In principle we should expect exact equality of v_out and v_out_expected,
  # but due to nondeterminism especially on GPU (e.g., due to convolution
  # autotuning) we only require "close".
  check_close(v_out, v_out_expected, atol=atol, rtol=rtol,
              err_msg=f'{err_msg} primal' if err_msg else 'primal')
  check_close(t_out, t_out_expected, atol=atol, rtol=rtol,
              err_msg=f'{err_msg} tangent' if err_msg else 'tangent')

