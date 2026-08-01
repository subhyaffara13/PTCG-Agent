
def array_split(ary: ArrayLike, indices_or_sections, axis=0):
    return _split_helper(ary, indices_or_sections, axis)


def array_split(ary, indices_or_sections, axis=0):
    """
    Split an array into multiple sub-arrays.

    Please refer to the ``split`` documentation.  The only difference
    between these functions is that ``array_split`` allows
    `indices_or_sections` to be an integer that does *not* equally
    divide the axis. For an array of length l that should be split
    into n sections, it returns l % n sub-arrays of size l//n + 1
    and the rest of size l//n.

    See Also
    --------
    split : Split array into multiple sub-arrays of equal size.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(8.0)
    >>> np.array_split(x, 3)
    [array([0.,  1.,  2.]), array([3.,  4.,  5.]), array([6.,  7.])]

    >>> x = np.arange(9)
    >>> np.array_split(x, 4)
    [array([0, 1, 2]), array([3, 4]), array([5, 6]), array([7, 8])]

    """
    try:
        Ntotal = ary.shape[axis]
    except AttributeError:
        Ntotal = len(ary)
    try:
        # handle array case.
        Nsections = len(indices_or_sections) + 1
        div_points = [0] + list(indices_or_sections) + [Ntotal]
    except TypeError:
        # indices_or_sections is a scalar, not an array.
        Nsections = int(indices_or_sections)
        if Nsections <= 0:
            raise ValueError('number sections must be larger than 0.') from None
        Neach_section, extras = divmod(Ntotal, Nsections)
        section_sizes = ([0] +
                         extras * [Neach_section + 1] +
                         (Nsections - extras) * [Neach_section])
        div_points = _nx.array(section_sizes, dtype=_nx.intp).cumsum()

    sub_arys = []
    sary = _nx.swapaxes(ary, axis, 0)
    for i in range(Nsections):
        st = div_points[i]
        end = div_points[i + 1]
        sub_arys.append(_nx.swapaxes(sary[st:end], axis, 0))

    return sub_arys


def array_split(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike,
                axis: int = 0) -> list[Array]:
  """Split an array into sub-arrays.

  JAX implementation of :func:`numpy.array_split`.

  Refer to the documentation of :func:`jax.numpy.split` for details; ``array_split``
  is equivalent to ``split``, but allows integer ``indices_or_sections`` which does
  not evenly divide the split axis.

  Examples:
    >>> x = jnp.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> chunks = jnp.array_split(x, 4)
    >>> print(*chunks)
    [1 2 3] [4 5] [6 7] [8 9]

  See also:
    - :func:`jax.numpy.split`: split an array along any axis.
    - :func:`jax.numpy.vsplit`: split vertically, i.e. along axis=0
    - :func:`jax.numpy.hsplit`: split horizontally, i.e. along axis=1
    - :func:`jax.numpy.dsplit`: split depth-wise, i.e. along axis=2
  """
  return _split("array_split", ary, indices_or_sections, axis=axis)

