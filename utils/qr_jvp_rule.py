
def qr_jvp_rule(primals, tangents, *, pivoting, full_matrices, use_magma):
  x, = primals
  dx, = tangents
  q, r, *p = qr_p.bind(x, pivoting=pivoting, full_matrices=full_matrices,
                       use_magma=use_magma)
  *_, m, n = x.shape
  if pivoting:
    dx = dx[..., p[0]]

  if m < n:
    # Wide matrix case (m < n)
    #
    # For wide matrices, we partition the input $X$ and the upper
    # trapezoidal matrix $R$ into square and remainder blocks:
    #
    # $$ X = \begin{bmatrix} X_1 & X_2 \end{bmatrix} $$
    # $$ R = \begin{bmatrix} R_1 & R_2 \end{bmatrix} $$
    #
    # where $X_1, R_1 \in \mathbb{C}^{m \times m}$ and
    # $X_2, R_2 \in \mathbb{C}^{m \times (n-m)}$.
    #
    # From the definition of the QR decomposition $X = QR$, we have:
    # $$ \begin{bmatrix} X_1 & X_2 \end{bmatrix} = Q \begin{bmatrix} R_1 & R_2 \end{bmatrix}
    #    = \begin{bmatrix} Q R_1 & Q R_2 \end{bmatrix} $$
    #
    # This separates into two equations:
    # 1)  $X_1 = Q R_1$
    # 2)  $X_2 = Q R_2$
    #
    # Equation (1) is exactly the QR decomposition of the square matrix $X_1$.
    # Therefore, we can compute $dQ$ and $dR_1$ by applying the standard
    # square QR derivative rules to $X_1$ and $dX_1$.
    #
    # For Equation (2), because $Q$ is unitary ($Q^H Q = I$), we can
    # isolate $R_2$:
    # $$ R_2 = Q^H X_2 $$
    #
    # Differentiating this expression via the product rule yields $dR_2$:
    # $$ dR_2 = (dQ)^H X_2 + Q^H dX_2 $$
    #
    # Finally, the full derivative $dR$ is formed by concatenating the blocks:
    # $$ dR = \begin{bmatrix} dR_1 & dR_2 \end{bmatrix} $$

    # Partition X = [X1, X2] where X1 is m x m
    # Partition R = [R1, R2] where R1 is m x m
    x2 = x[..., :, m:]
    dx1 = dx[..., :, :m]
    dx2 = dx[..., :, m:]
    r1 = r[..., :, :m]

    # Use thin QR JVP for the square part X1 = Q R1
    dq, dr1 = _thin_qr_jvp(q, r1, dx1)

    # Compute dR2 = (dQ^H) X2 + Q^H dX2
    dr2 = _H(dq) @ x2 + _H(q) @ dx2

    # Concatenate to form the full m x n dR matrix
    last_dim = len(dr1.shape) - 1
    dr = lax.concatenate((dr1, dr2), last_dim)

    if pivoting:
      dp = ad_util.p2tz(p[0])
      return (q, r, p[0]), (dq, dr, dp)
    return (q, r), (dq, dr)

  q_mn = q[..., :, :n] if full_matrices else q
  r_nn = r[..., :n, :n] if full_matrices else r

  dq_mn, dr_nn = _thin_qr_jvp(q_mn, r_nn, dx)

  if not full_matrices or m == n:
    dq = dq_mn
    dr = dr_nn
  else:
    # See https://arxiv.org/pdf/2409.13374 for the full matrices derivation.
    q_nn = q_mn[..., :n, :]
    q_pn = q_mn[..., n:, :]
    q_mp = q[..., :, n:]

    dq_nn = dq_mn[..., :n, :]
    dq_pn = dq_mn[..., n:, :]

    # Eq 33: Z_pn = Q_pn @ (Q_nn - I)^{-1}
    # To avoid explicit inversion, we compute Z_pn using a linear system solve:
    # (Q_nn - I)^H @ Z_pn^H = Q_pn^H  =>  Z_pn^H = solve((Q_nn - I)^H, Q_pn^H)
    I_n = lax.expand_dims(lax._eye(q_nn.dtype, (n, n)), range(q_nn.ndim - 2))
    lu_factor, _, perm = lu(q_nn - I_n)
    z_pn_H = lu_solve(lu_factor, perm, _H(q_pn), trans=2) # trans=2 solves A^H X = B
    z_pn = _H(z_pn_H)

    # Eq 32: dq_mp = dq_mn @ Z_pn^H - (Q_mn + Q_mp @ Z_pn) @ (dq_pn - Z_pn @ dq_nn)^H
    dq_mp = dq_mn @ z_pn_H - (q_mn + q_mp @ z_pn) @ _H(dq_pn - z_pn @ dq_nn)

    last_dim = len(dq_mn.shape) - 1
    dq = lax.concatenate((dq_mn, dq_mp), last_dim)

    zeros = lax.full((*dr_nn.shape[:-2], m - n, n), 0, dtype=dr_nn.dtype)
    second_last_dim = len(dr_nn.shape) - 2
    dr = lax.concatenate((dr_nn, zeros), second_last_dim)

  if pivoting:
    dp = ad_util.p2tz(p[0])
    return (q, r, p[0]), (dq, dr, dp)
  return (q, r), (dq, dr)

