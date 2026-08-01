
def _lu(a: ArrayLike, permute_l: Literal[True]) -> tuple[Array, Array]: ...


def _lu(a: ArrayLike, permute_l: Literal[False]) -> tuple[Array, Array, Array]: ...


def _lu(a: ArrayLike, permute_l: bool) -> tuple[Array, Array] | tuple[Array, Array, Array]: ...


def _lu(a: ArrayLike, permute_l: bool) -> tuple[Array, Array] | tuple[Array, Array, Array]:
  a, = promote_dtypes_inexact(jnp.asarray(a))
  lu, _, permutation = lax_linalg.lu(a)
  dtype = lax.dtype(a)
  m, n = np.shape(a)
  p = jnp.real(jnp.array(permutation[None, :] == jnp.arange(m, dtype=permutation.dtype)[:, None], dtype=dtype))
  k = min(m, n)
  l = jnp.tril(lu, -1)[:, :k] + jnp.eye(m, k, dtype=dtype)
  u = jnp.triu(lu)[:k, :]
  if permute_l:
    return jnp.matmul(p, l, precision=lax.Precision.HIGHEST), u
  else:
    return p, l, u

