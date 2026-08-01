
def _pinv_jvp(rtol, hermitian, primals, tangents):
  # The Differentiation of Pseudo-Inverses and Nonlinear Least Squares Problems
  # Whose Variables Separate. Author(s): G. H. Golub and V. Pereyra. SIAM
  # Journal on Numerical Analysis, Vol. 10, No. 2 (Apr., 1973), pp. 413-432.
  # (via https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse#Derivative)
  a, = primals  # m x n
  a_dot, = tangents
  p = pinv(a, rtol=rtol, hermitian=hermitian)  # n x m
  if hermitian:
    # svd(..., hermitian=True) symmetrizes its input, and the JVP must match.
    a = _symmetrize(a)
    a_dot = _symmetrize(a_dot)

  # TODO(phawkins): this could be simplified in the Hermitian case if we
  # supported triangular matrix multiplication.
  m, n = a.shape[-2:]
  if m >= n:
    s = (p @ _H(p)) @ _H(a_dot)  # nxm
    t = (_H(a_dot) @ _H(p)) @ p  # nxm
    p_dot = -(p @ a_dot) @ p + s - (s @ a) @ p + t - (p @ a) @ t
  else:  # m < n
    s = p @ (_H(p) @ _H(a_dot))
    t = _H(a_dot) @ (_H(p) @ p)
    p_dot = -p @ (a_dot @ p) + s - s @ (a @ p) + t - p @ (a @ t)
  return p, p_dot

