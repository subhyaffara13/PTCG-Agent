
def _gmm_fwd(
    lhs: jnp.ndarray,
    rhs: jnp.ndarray,
    group_sizes: jnp.ndarray,
    preferred_element_type: jnp.dtype = jnp.float32,
    tiling: tuple[int, int, int] = (128, 128, 128),
    group_offset: jnp.ndarray | None = None,
    existing_out: jnp.ndarray | None = None,
    transpose_rhs: bool = False,
    interpret: bool = False,
) -> tuple[
    jnp.ndarray,
    tuple[
        jnp.ndarray,
        jnp.ndarray,
        jnp.ndarray,
        jnp.ndarray | None,
        int,
    ],
]:
  """Forward function for GMM VJP."""
  out = backend.gmm(
      lhs,
      rhs,
      group_sizes,
      preferred_element_type,
      tiling,
      group_offset,
      existing_out,
      transpose_rhs=transpose_rhs,
      interpret=interpret,
  )
  return out, (lhs, rhs, group_sizes, group_offset, rhs.shape[0])

