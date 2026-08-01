
def binary_ufunc(identity: Any, reduce: Callable[..., Any] | None = None,
                 accumulate: Callable[..., Any] | None = None,
                 at: Callable[..., Any] | None = None,
                 reduceat: Callable[..., Any] | None = None) -> Callable[[Callable[[ArrayLike, ArrayLike], Array]], ufunc]:
  """An internal helper function for defining binary ufuncs."""
  def decorator(func: Callable[[ArrayLike, ArrayLike], Array]) -> ufunc:
    func_jit = jit(func, inline=True)
    return ufunc(func_jit, name=func.__name__, nin=2, nout=1, call=func_jit,
                 identity=identity, reduce=reduce, accumulate=accumulate, at=at, reduceat=reduceat)
  return decorator

