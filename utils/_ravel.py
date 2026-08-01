
def _ravel(M):
    if hasattr(M, 'toarray'):
        return M.toarray().ravel()
    elif hasattr(M, 'A'):
        return M.A.ravel()
    else:
        return M.ravel()


def _ravel(p: Any) -> jax.Array:
  return flatten_util.ravel_pytree(p)[0]

