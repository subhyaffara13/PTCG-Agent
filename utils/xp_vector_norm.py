
def xp_vector_norm(x: Array, /, *,
                   axis: int | tuple[int, int] | None = None,
                   keepdims: bool = False,
                   ord: int | float = 2,
                   xp: ModuleType | None = None) -> Array:
    xp = array_namespace(x) if xp is None else xp

    if SCIPY_ARRAY_API:
        # check for optional `linalg` extension
        if hasattr(xp, 'linalg'):
            return xp.linalg.vector_norm(x, axis=axis, keepdims=keepdims, ord=ord)
        else:
            if ord != 2:
                raise ValueError(
                    "only the Euclidean norm (`ord=2`) is currently supported in "
                    "`xp_vector_norm` for backends not implementing the `linalg` "
                    "extension."
                )
            # return (x @ x)**0.5
            # or to get the right behavior with nd, complex arrays
            return xp.sum(xp.conj(x) * x, axis=axis, keepdims=keepdims)**0.5
    else:
        # to maintain backwards compatibility
        return np.linalg.norm(x, ord=ord, axis=axis, keepdims=keepdims)

