
def check_grads(f, args, order,
                modes=("fwd", "rev"), atol=None, rtol=None, eps=None):
  """Check gradients from automatic differentiation against finite differences.

  Gradients are only checked in a single randomly chosen direction, which
  ensures that the finite difference calculation does not become prohibitively
  expensive even for large input/output spaces.

  Args:
    f: function to check at ``f(*args)``.
    args: tuple of argument values.
    order: forward and backwards gradients up to this order are checked.
    modes: lists of gradient modes to check ('fwd' and/or 'rev').
    atol: absolute tolerance for gradient equality.
    rtol: relative tolerance for gradient equality.
    eps: step size used for finite differences.

  Raises:
    AssertionError: if gradients do not match.
  """
  args = tuple(args)
  eps = eps or EPS

  _check_jvp = partial(check_jvp, atol=atol, rtol=rtol, eps=eps)
  _check_vjp = partial(check_vjp, atol=atol, rtol=rtol, eps=eps)

  def _check_grads(f, args, order, err_msg=''):
    if "fwd" in modes:
      fwd_msg = f'JVP of {err_msg}' if err_msg else 'JVP'
      _check_jvp(f, partial(api.jvp, f), args, err_msg=fwd_msg)
      if order > 1:
        _check_grads(partial(api.jvp, f), (args, args), order - 1, fwd_msg)

    if "rev" in modes:
      rev_msg = f'VJP of {err_msg}' if err_msg else 'VJP'
      _check_vjp(f, partial(api.vjp, f), args, err_msg=rev_msg)
      if order > 1:
        def f_vjp(*args):
          out_primal_py, vjp_py = api.vjp(f, *args)
          return vjp_py(out_primal_py)
        _check_grads(f_vjp, args, order - 1, rev_msg)

    if "lin" in modes:
      lin_msg = f'LIN of {err_msg}' if err_msg else 'LIN'
      _check_jvp(f, partial(_jvp_from_lin, f), args, err_msg=lin_msg)
      if order > 1:
        _check_grads(partial(_jvp_from_lin, f), (args, args), order - 1, lin_msg)

  _check_grads(f, args, order)

