
def _split(x, indices_or_sections, axis, xp):
    """A simplified version of np.split, with `indices` being a list.
    """
    # https://github.com/numpy/numpy/blob/v2.2.0/numpy/lib/_shape_base_impl.py#L743
    Ntotal = x.shape[axis]

    # handle array case.
    Nsections = len(indices_or_sections) + 1
    div_points = [0] + list(indices_or_sections) + [Ntotal]

    sub_arys = []
    sary = xp_swapaxes(x, axis, 0, xp=xp)
    for i in range(Nsections):
        st = div_points[i]
        end = div_points[i + 1]
        sub_arys.append(xp_swapaxes(sary[st:end, ...], axis, 0, xp=xp))

    return sub_arys


def _split(x, t, k, residuals):
    """Split the knot interval into "runs".
    """
    ix = np.searchsorted(x, t[k:-k])
    # sum half-open intervals
    fparts = [residuals[ix[i]:ix[i+1]].sum() for i in range(len(ix)-1)]
    carries = residuals[ix[1:-1]]

    for i in range(len(carries)):     # split residuals at internal knots
        carry = carries[i] / 2
        fparts[i] += carry
        fparts[i+1] -= carry

    fparts[-1] += residuals[-1]       # add the contribution of the last knot

    xp_assert_close(sum(fparts), sum(residuals), atol=1e-15)

    return fparts, ix


def _split(a, sep=None, maxsplit=None):
    """
    For each element in `a`, return a list of the words in the
    string, using `sep` as the delimiter string.

    Calls :meth:`str.split` element-wise.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype

    sep : str or unicode, optional
       If `sep` is not specified or None, any whitespace string is a
       separator.

    maxsplit : int, optional
        If `maxsplit` is given, at most `maxsplit` splits are done.

    Returns
    -------
    out : ndarray
        Array of list objects

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array("Numpy is nice!")
    >>> np.strings.split(x, " ")  # doctest: +SKIP
    array(list(['Numpy', 'is', 'nice!']), dtype=object)  # doctest: +SKIP

    >>> np.strings.split(x, " ", 1)  # doctest: +SKIP
    array(list(['Numpy', 'is nice!']), dtype=object)  # doctest: +SKIP

    See Also
    --------
    str.split, rsplit

    """
    # This will return an array of lists of different sizes, so we
    # leave it as an object array
    return _vec_string(
        a, np.object_, 'split', [sep] + _clean_args(maxsplit))


def _split(x, indices, axis):
  if isinstance(x, np.ndarray):
    return np.split(x, indices, axis)
  else:
    return x._split(indices, axis)


def _split(op: str, ary: ArrayLike,
           indices_or_sections: int | Sequence[int] | ArrayLike,
           axis: int = 0) -> list[Array]:
  ary = util.ensure_arraylike(op, ary)
  axis = core.concrete_or_error(operator.index, axis, f"in jax.numpy.{op} argument `axis`")
  size = ary.shape[axis]
  if (isinstance(indices_or_sections, (tuple, list)) or
      isinstance(indices_or_sections, (np.ndarray, Array)) and
      indices_or_sections.ndim > 0):
    split_indices = np.asarray([0] + [
        core.concrete_dim_or_error(i_s, f"in jax.numpy.{op} argument 1")
        for i_s in indices_or_sections] + [size])
    sizes = list(np.diff(split_indices))
  else:
    if core.is_symbolic_dim(indices_or_sections):
      raise ValueError(f"jax.numpy.{op} with a symbolic number of sections is "
                       "not supported")
    num_sections: int = core.concrete_or_error(int, indices_or_sections,
                                               f"in jax.numpy.{op} argument 1")
    part_size, r = divmod(size, num_sections)
    if r == 0:
      sizes = [part_size] * num_sections
    elif op == "array_split":
      sizes = [(part_size + 1)] * r + [part_size] * (num_sections - r)
    else:
      raise ValueError(f"array split does not result in an equal division: rest is {r}")
  sizes = [i if core.is_symbolic_dim(i) else np.int64(i)
           for i in sizes]
  return list(lax.split(ary, sizes, axis=axis))


def _split(key: Array, num: int | tuple[int, ...] = 2) -> Array:
  # Alternative to split() to use within random samplers.
  # TODO(frostig): remove and use split(); we no longer need to wait
  # to always enable_custom_prng
  assert dtypes.issubdtype(key.dtype, dtypes.prng_key)
  if key.ndim:
    raise TypeError("split accepts a single key, but was given a key array of "
                    f"shape {key.shape} != (). Use jax.vmap for batching.")
  shape = tuple(num) if isinstance(num, Sequence) else (num,)
  return prng.random_split(key, shape=shape)


def _split(key: typing.Array, shape: Shape):
  del key, shape
  raise NotImplementedError(
      "Cannot split a Pallas key. Use fold_in instead to generate new keys."
  )

