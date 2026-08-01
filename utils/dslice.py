
def dslice(
    start: int | Array | None,
    size: int | Array | None = None,
    stride: int | None = None,
) -> slice | Slice:
  """Constructs a ``Slice`` from a start index and a size.

  The semantics of ``dslice`` mirror those of the builtin ``slice`` type:

  * ``dslice(None)`` is ``:``
  * ``dslice(j)`` is ``:j``
  * ``dslice(i, j)`` is ``i:i+j``
  * ``dslice(i, j, stride)`` is ``i:i+j:stride``

  Examples:

    >>> x = jax.numpy.arange(10)
    >>> i = 4
    >>> x[i: i + 2]  # standard indexing requires i to be static
    Array([4, 5], dtype=int32)
    >>> x[jax.ds(i, 2)]  # equivalent which allows i to be dynamic
    Array([4, 5], dtype=int32)

    Here is an explicit example of slicing with a dynamic start index:

    >>> @jax.jit(static_argnames='size')
    ... def f(x, i, size):  # example of when `
    ...   return x[jax.ds(i, size)]
    ...
    >>> f(x, i, 2)
    Array([4, 5], dtype=int32)
  """
  if start is None:
    return slice(None)
  if stride is None:
    stride = 1
  if not isinstance(stride, int):
    raise ValueError("Non-static stride in `dslice`")
  if size is None:
    start, size = 0, start
  return Slice(start, size, stride)

