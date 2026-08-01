
def _eigh_jvp_rule(
    primals, tangents, *, lower, sort_eigenvalues, subset_by_index, algorithm
):
  (a,) = primals
  n = a.shape[-1]
  if not (subset_by_index is None or subset_by_index == (0, n)):
    raise NotImplementedError(
        "Derivatives not defined for partial eigen decomposition."
    )
  # Derivative for eigh in the simplest case of distinct eigenvalues.
  # This is classic nondegenerate perurbation theory, but also see
  # https://people.maths.ox.ac.uk/gilesm/files/NA-08-01.pdf
  # The general solution treating the case of degenerate eigenvalues is
  # considerably more complicated. Ambitious readers may refer to the general
  # methods below or refer to degenerate perturbation theory in physics.
  # https://www.win.tue.nl/analysis/reports/rana06-33.pdf and
  # https://people.orie.cornell.edu/aslewis/publications/99-clarke.pdf
  a_dot, = tangents

  v, w_real = eigh_p.bind(
      symmetrize(a),
      lower=lower,
      sort_eigenvalues=sort_eigenvalues,
      subset_by_index=subset_by_index,
      algorithm=algorithm,
  )

  # for complex numbers we need eigenvalues to be full dtype of v, a:
  w = w_real.astype(a.dtype)
  eye_n = lax._eye(a.dtype, (n, n))
  # carefully build reciprocal delta-eigenvalue matrix, avoiding NaNs.
  with config.numpy_rank_promotion("allow"):
    Fmat = lax.integer_pow(eye_n + w[..., np.newaxis, :] - w[..., np.newaxis], -1) - eye_n
  # eigh impl doesn't support batch dims, but future-proof the grad.
  dot = partial(lax.dot if a.ndim == 2 else lax.batch_matmul,
                precision=lax.Precision.HIGHEST)
  vdag_adot_v = dot(dot(_H(v), a_dot), v)
  dv = dot(v, Fmat * vdag_adot_v)
  dw = _extract_diagonal(vdag_adot_v.real)
  return (v, w_real), (dv, dw)

