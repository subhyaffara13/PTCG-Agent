
def _svd(x: ArrayLike, *, full_matrices: bool, compute_uv: Literal[True]) -> tuple[Array, Array, Array]: ...


def _svd(x: ArrayLike, *, full_matrices: bool, compute_uv: Literal[False]) -> Array: ...


def _svd(x: ArrayLike, *, full_matrices: bool, compute_uv: bool) -> Array | tuple[Array, Array, Array]: ...


def _svd(a: ArrayLike, *, full_matrices: bool, compute_uv: bool) -> Array | tuple[Array, Array, Array]:
  a, = promote_dtypes_inexact(jnp.asarray(a))
  return lax_linalg.svd(a, full_matrices=full_matrices, compute_uv=compute_uv)

