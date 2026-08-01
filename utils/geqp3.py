
def geqp3(a: ArrayLike, jpvt: ArrayLike, *,
          use_magma: bool | None = None) -> tuple[Array, Array, Array]:
  """Computes the column-pivoted QR decomposition of a matrix.

  Args:
    a: a ``[..., m, n]`` batch of matrices, with floating-point or complex type.
    jpvt: a ``[..., n]`` batch of column-pivot index vectors with integer type,
    use_magma: Locally override the ``jax_use_magma`` flag. If ``True``, the
      `geqp3` is computed using MAGMA. If ``False``, the computation is done using
      LAPACK on to the host CPU. If ``None`` (default), the behavior is controlled
      by the ``jax_use_magma`` flag. This argument is only used on GPU.
  Returns:
    A ``(a, jpvt, taus)`` triple, where ``r`` is in the upper triangle of ``a``,
    ``q`` is represented in the lower triangle of ``a`` and in ``taus`` as
    elementary Householder reflectors, and ``jpvt`` is the column-pivot indices
    such that ``a[:, jpvt] = q @ r``.
  """
  a, jpvt = core.auto_insert_reshard(a, jpvt)
  a_out, jpvt_out, taus = geqp3_p.bind(a, jpvt, use_magma=use_magma)
  return a_out, jpvt_out, taus

