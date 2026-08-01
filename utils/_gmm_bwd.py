
def _gmm_bwd(
    preferred_element_type: jnp.dtype,
    tiling: tuple[int, int, int],
    transpose_rhs: bool,
    interpret: bool,
    residual: tuple[
        jnp.ndarray,
        jnp.ndarray,
        jnp.ndarray,
        jnp.ndarray | None,
        int,
    ],
    grad: jnp.ndarray,
) -> tuple[jnp.ndarray, jnp.ndarray, None, None, jnp.ndarray]:
  """Backward function for throughput GMM VJP."""
  del preferred_element_type
  lhs, rhs, group_sizes, group_offset, num_actual_groups = residual
  grad_lhs = backend.gmm(
      grad,
      rhs,
      group_sizes,
      lhs[0].dtype,
      tiling,
      group_offset,
      transpose_rhs=not transpose_rhs,
      interpret=interpret,
  )
  grad_rhs = backend.tgmm(
      lhs.swapaxes(0, 1),
      grad,
      group_sizes,
      rhs.dtype,
      tiling,
      group_offset,
      num_actual_groups,
      interpret=interpret,
  )

  # NOTE: If the rhs transposition is fused into the forward pass we need to
  # return the transpose of the rhs gradient that we calculated above.
  #
  # TODO(tgale, enriqueps, apaske): Fuse this transposition into the tgmm.
  grad_rhs = grad_rhs.swapaxes(1, 2) if transpose_rhs else grad_rhs
  return grad_lhs, grad_rhs, None, None, grad

