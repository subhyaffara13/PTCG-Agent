
def eig_jvp_rule(primals, tangents, *, compute_left_eigenvectors,
                 compute_right_eigenvectors, enable_eigvec_derivs,
                 implementation):
  a, = primals
  da, = tangents
  if compute_left_eigenvectors or compute_right_eigenvectors:
    if not enable_eigvec_derivs:
      raise NotImplementedError(
          'Derivatives of non-symmetric eigenvectors are only valid under '
          'assumptions on the input that JAX cannot check (see the '
          'enable_eigvec_derivs argument to jax.lax.linalg.eig). Pass '
          'enable_eigvec_derivs=True to jax.lax.linalg.eig to opt in. See '
          'https://github.com/jax-ml/jax/issues/2748 for discussion.')
  outs = eig(a, compute_left_eigenvectors=compute_left_eigenvectors,
             compute_right_eigenvectors=True,
             enable_eigvec_derivs=enable_eigvec_derivs,
             implementation=implementation)
  w, vr = outs[0], outs[-1]
  dot = partial(lax.dot if a.ndim == 2 else lax.batch_matmul,
                precision=lax.Precision.HIGHEST)
  da = da.astype(vr.dtype)
  if not (compute_left_eigenvectors or compute_right_eigenvectors):
    return [w], [(_solve(vr, da) * _T(vr)).sum(-1)]
  dw, dvr = _eig_vec_jvp(dot, w, vr, da)
  primal_out, tangent_out = [w], [dw]
  if compute_left_eigenvectors:
    vl = outs[1]
    _, dvl = _eig_vec_jvp(dot, w.conj(), vl, _H(da))
    primal_out.append(vl)
    tangent_out.append(dvl)
  if compute_right_eigenvectors:
    primal_out.append(vr)
    tangent_out.append(dvr)
  return primal_out, tangent_out

