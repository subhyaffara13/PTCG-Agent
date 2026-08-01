
def _tridiagonal_solve_jax_impl(dl, d, du, b):
  def fwd(carry, args):
    cp, dp = carry
    a, b, c, d = args
    cp_next = c / (b - a * cp)
    dp_next = (d - a * dp) / (b - a * cp)
    return (cp_next, dp_next), (cp, dp)

  (_, final), (cp, dp) = control_flow.scan(
      fwd, (du[0] / d[0], b[0] / d[0]), (dl[1:], d[1:], du[1:], b[1:, :]),
      unroll=32)

  def bwd(xn, args):
    cp, dp = args
    x = dp - cp * xn
    return x, xn

  end, ans = control_flow.scan(bwd, final, (cp, dp), unroll=32, reverse=True)
  return lax.concatenate((end[None], ans), 0)

