
def _eigh(a: ArrayLike, b: ArrayLike | None, lower: bool, eigvals_only: Literal[True],
          eigvals: None, type: int) -> Array: ...


def _eigh(a: ArrayLike, b: ArrayLike | None, lower: bool, eigvals_only: Literal[False],
          eigvals: None, type: int) -> tuple[Array, Array]: ...


def _eigh(a: ArrayLike, b: ArrayLike | None, lower: bool, eigvals_only: bool,
          eigvals: None, type: int) -> Array | tuple[Array, Array]: ...


def _eigh(a: ArrayLike, b: ArrayLike | None, lower: bool, eigvals_only: bool,
          eigvals: None, type: int) -> Array | tuple[Array, Array]:
  if b is not None:
    raise NotImplementedError("Only the b=None case of eigh is implemented")
  if type != 1:
    raise NotImplementedError("Only the type=1 case of eigh is implemented.")
  if eigvals is not None:
    raise NotImplementedError(
        "Only the eigvals=None case of eigh is implemented.")

  a, = promote_dtypes_inexact(jnp.asarray(a))
  v, w = lax_linalg.eigh(a, lower=lower)

  if eigvals_only:
    return w
  else:
    return w, v

