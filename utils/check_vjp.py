
def check_vjp(f, f_vjp, args, atol=None, rtol=None, eps=EPS, err_msg=''):
  """Check a VJP from automatic differentiation against finite differences.

  Gradients are only checked in a single randomly chosen direction, which
  ensures that the finite difference calculation does not become prohibitively
  expensive even for large input/output spaces.

  Args:
    f: function to check at ``f(*args)``.
    f_vjp: function that calculates ``jax.vjp`` applied to ``f``. Typically this
      should be ``functools.partial(jax.vjp, f)``.
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
  _rand_like = partial(rand_like, np.random.RandomState(0))
  v_out, vjpfun = f_vjp(*args)
  v_out_expected = f(*args)
  check_close(v_out, v_out_expected, atol=atol, rtol=rtol,
              err_msg=f'{err_msg} primal' if err_msg else 'primal')
  tangent = tree_map(_rand_like, args)
  tangent_out = numerical_jvp(f, args, tangent, eps=eps)
  cotangent = tree_map(_rand_like, v_out)
  cotangent_out = conj(vjpfun(conj(cotangent)))
  ip = inner_prod(tangent, cotangent_out)
  ip_expected = inner_prod(tangent_out, cotangent)
  check_close(ip, ip_expected, atol=atol, rtol=rtol,
              err_msg=(f'{err_msg} cotangent projection'
                       if err_msg else 'cotangent projection'))

