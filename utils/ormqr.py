
def ormqr(
    input: Tensor,
    tau: Tensor,
    other: Tensor,
    left: bool = True,
    transpose: bool = False,
) -> Tensor:
    torch._check(
        input.ndim >= 2, lambda: "torch.ormqr: input must have at least 2 dimensions."
    )
    torch._check(
        other.ndim >= 2, lambda: "torch.ormqr: other must have at least 2 dimensions."
    )

    left_size_condition = -2 if left else -1
    torch._check(
        other.shape[left_size_condition] >= tau.shape[-1],
        lambda: f"torch.ormqr: other.shape[{left_size_condition}] must be greater than or equal to tau.shape[-1]",
    )
    torch._check(
        other.shape[left_size_condition] == input.shape[-2],
        lambda: f"torch.ormqr: other.shape[{left_size_condition}] must be equal to input.shape[-2]",
    )

    torch._check(
        tau.shape[-1] <= input.shape[-1],
        lambda: "torch.ormqr: tau.shape[-1] must be less than or equal to input.shape[-1]",
    )

    torch._check(
        input.ndim - tau.ndim == 1,
        lambda: (
            f"torch.ormqr: Expected tau to have one dimension less than input, "
            f"but got tau.ndim equal to {tau.ndim} and input.ndim is equal to {input.ndim}"
        ),
    )
    torch._check(
        input.ndim == other.ndim,
        lambda: (
            f"torch.ormqr: Expected other to have the same number of dimensions as input, "
            f"but got other.ndim equal to {other.ndim} and input.ndim is equal to {input.ndim}"
        ),
    )

    if input.ndim > 2:
        expected_batch_shape = input.shape[:-2]
        actual_batch_tau_shape = tau.shape[:-1]
        torch._check(
            actual_batch_tau_shape == expected_batch_shape,
            lambda: (
                f"torch.ormqr: Expected batch dimensions of tau to be "
                f"equal to input.shape[:-2], but got {actual_batch_tau_shape}"
            ),
        )

        actual_batch_other_shape = other.shape[:-2]
        torch._check(
            actual_batch_other_shape == expected_batch_shape,
            lambda: (
                f"torch.ormqr: Expected batch dimensions of other to be "
                f"equal to input.shape[:-2], but got {actual_batch_other_shape}"
            ),
        )

    torch._check(
        tau.dtype == input.dtype,
        lambda: (
            f"torch.ormqr: Expected input and tau to have the same dtype, "
            f"but input has dtype {input.dtype} and tau has dtype {tau.dtype}"
        ),
    )
    torch._check(
        other.dtype == input.dtype,
        lambda: (
            f"torch.ormqr: Expected input and other to have the same dtype, "
            f"but input has dtype {input.dtype} and other has dtype {other.dtype}"
        ),
    )

    checkSameDevice("torch.ormqr", tau, input, "tau")
    checkSameDevice("torch.ormqr", other, input, "other")

    return torch.empty_strided(
        size=other.shape,
        stride=make_contiguous_strides_for(other.shape, row_major=False),
        dtype=other.dtype,
        device=other.device,
    )


def ormqr(a: ArrayLike, taus: ArrayLike, c: ArrayLike, *,
          left: bool = True, transpose: bool = False) -> Array:
  """Multiplies a matrix by Q from a QR factorization without materializing Q.

  Computes ``Q @ C`` (``left=True``, ``transpose=False``),
  ``Q^T @ C`` (``left=True``, ``transpose=True``),
  ``C @ Q`` (``left=False``, ``transpose=False``), or
  ``C @ Q^T`` (``left=False``, ``transpose=True``).

  For complex types, ``transpose=True`` computes the conjugate transpose
  (``Q^H``).

  Args:
    a: The Householder reflectors with shape ``[..., m, n]``, as returned by
      the internal ``geqrf``/``geqp3`` primitives. Alternatively, one can use
      :func:`jax.numpy.linalg.qr` with ``mode="raw"``, but in this case the
      returned ``a`` must be transposed with ``.mT`` (see example below).
    taus: The Householder scalar factors with shape ``[..., k]``, as returned
      by ``geqrf``/``geqp3`` or the second element of the tuple from
      :func:`jax.numpy.linalg.qr` with ``mode="raw"``.
    c: The matrix to multiply by Q, with shape ``[..., c_rows, c_cols]``.
    left: If ``True``, compute ``Q @ C``. If ``False``, compute ``C @ Q``.
    transpose: If ``True``, use ``Q^T`` (or ``Q^H`` for complex types).

  Returns:
    The result of multiplying ``c`` by Q (or ``Q^T``/``Q^H``), with the
    same shape as ``c``.

  Examples:
    Multiply a vector by Q without forming Q explicitly:

    >>> import jax.numpy as jnp
    >>> from jax.lax.linalg import ormqr
    >>> a = jnp.array([[1., 2.], [3., 4.], [5., 6.]])
    >>> h, taus = jnp.linalg.qr(a, mode="raw")
    >>> c = jnp.eye(3)
    >>> Q_times_c = ormqr(h.mT, taus, c)
    >>> Q_direct, _ = jnp.linalg.qr(a, mode="complete")
    >>> jnp.allclose(Q_times_c, Q_direct, atol=1e-5)
    Array(True, dtype=bool)

  See also:
    - :func:`jax.scipy.linalg.qr_multiply`: Higher-level API for computing
      Q @ C or C @ Q from a matrix ``a`` directly.
  """
  a, taus, c = core.auto_insert_reshard(a, taus, c)
  return ormqr_p.bind(a, taus, c, left=left, transpose=transpose)

