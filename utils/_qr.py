
def _qr(a: ArrayLike, mode: Literal["r"], pivoting: Literal[False]
       ) -> tuple[Array]: ...


def _qr(a: ArrayLike, mode: Literal["r"], pivoting: Literal[True]
       ) -> tuple[Array, Array]: ...


def _qr(a: ArrayLike, mode: Literal["full", "economic"], pivoting: Literal[False]
       ) -> tuple[Array, Array]: ...


def _qr(a: ArrayLike, mode: Literal["full", "economic"], pivoting: Literal[True]
       ) -> tuple[Array, Array, Array]: ...


def _qr(a: ArrayLike, mode: str, pivoting: Literal[False]
       ) -> tuple[Array] | tuple[Array, Array]: ...


def _qr(a: ArrayLike, mode: str, pivoting: Literal[True]
       ) -> tuple[Array, Array] | tuple[Array, Array, Array]: ...


def _qr(a: ArrayLike, mode: str, pivoting: bool
       ) -> tuple[Array] | tuple[Array, Array] | tuple[Array, Array, Array]: ...


def _qr(a: ArrayLike, mode: str, pivoting: bool
       ) -> tuple[Array] | tuple[Array, Array] | tuple[Array, Array, Array]:
  if mode in ("full", "r"):
    full_matrices = True
  elif mode == "economic":
    full_matrices = False
  else:
    raise ValueError(f"Unsupported QR decomposition mode '{mode}'")
  a, = promote_dtypes_inexact(jnp.asarray(a))
  q, r, *p = lax_linalg.qr(a, pivoting=pivoting, full_matrices=full_matrices)
  if mode == "r":
    if pivoting:
      return r, p[0]
    return (r,)
  if pivoting:
    return q, r, p[0]
  return q, r

