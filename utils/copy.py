
def copy(obj, *args, **kwds):
    """
    Use pickling to 'copy' an object (i.e. `loads(dumps(obj))`).

    See :func:`dumps` and :func:`loads` for keyword arguments.
    """
    ignore = kwds.pop('ignore', Unpickler.settings['ignore'])
    return loads(dumps(obj, *args, **kwds), ignore=ignore)


def copy(src, dst, overwrite=False):
  if io_mode == BackendMode.DEFAULT:
    if os.path.exists(dst) and not overwrite:
      raise errors.AlreadyExistsError(dst)
    shutil.copy(src, dst)
    return
  elif io_mode == BackendMode.TF:
    return gfile.copy(src, dst, overwrite=overwrite)
  else:
    raise ValueError('Unknown IO Backend Mode.')


def copy(source):
    """Copy a docstring from another source function (if present)."""
    def do_copy(target):
        if source.__doc__:
            target.__doc__ = source.__doc__
        return target
    return do_copy


def copy(self, src, non_blocking=False):
    if not isinstance(src, ir.IRNode):
        src = tensor(src, dtype=self.get_dtype(), device=self.get_device())
    x = src
    if self.get_device() != src.get_device():
        x = to_device(x, self.get_device())
    if self.get_dtype() != src.get_dtype():
        x = to_dtype(x, self.get_dtype())

    if self.get_size() != src.get_size():
        out = expand(x, self.get_size())
        return clone(out)
    return clone(x)


def copy(
    a: ArrayLike, order: NotImplementedType = "K", subok: NotImplementedType = False
):
    return a.clone()


def copy(src, dst, only_update=False, copystat=True, cwd=None,
         dest_is_dir=False, create_dest_dirs=False):
    """ Variation of ``shutil.copy`` with extra options.

    Parameters
    ==========

    src : str
        Path to source file.
    dst : str
        Path to destination.
    only_update : bool
        Only copy if source is newer than destination
        (returns None if it was newer), default: ``False``.
    copystat : bool
        See ``shutil.copystat``. default: ``True``.
    cwd : str
        Path to working directory (root of relative paths).
    dest_is_dir : bool
        Ensures that dst is treated as a directory. default: ``False``
    create_dest_dirs : bool
        Creates directories if needed.

    Returns
    =======

    Path to the copied file.

    """
    if cwd:  # Handle working directory
        if not os.path.isabs(src):
            src = os.path.join(cwd, src)
        if not os.path.isabs(dst):
            dst = os.path.join(cwd, dst)

    if not os.path.exists(src):  # Make sure source file exists
        raise FileNotFoundError("Source: `{}` does not exist".format(src))

    # We accept both (re)naming destination file _or_
    # passing a (possible non-existent) destination directory
    if dest_is_dir:
        if not dst[-1] == '/':
            dst = dst+'/'
    else:
        if os.path.exists(dst) and os.path.isdir(dst):
            dest_is_dir = True

    if dest_is_dir:
        dest_dir = dst
        dest_fname = os.path.basename(src)
        dst = os.path.join(dest_dir, dest_fname)
    else:
        dest_dir = os.path.dirname(dst)

    if not os.path.exists(dest_dir):
        if create_dest_dirs:
            make_dirs(dest_dir)
        else:
            raise FileNotFoundError("You must create directory first.")

    if only_update:
        if not missing_or_other_newer(dst, src):
            return

    if os.path.islink(dst):
        dst = os.path.abspath(os.path.realpath(dst), cwd=cwd)

    shutil.copy(src, dst)
    if copystat:
        shutil.copystat(src, dst)

    return dst


def copy(a, order='K', subok=False):
    """
    Return an array copy of the given object.

    Parameters
    ----------
    a : array_like
        Input data.
    order : {'C', 'F', 'A', 'K'}, optional
        Controls the memory layout of the copy. 'C' means C-order,
        'F' means F-order, 'A' means 'F' if `a` is Fortran contiguous,
        'C' otherwise. 'K' means match the layout of `a` as closely
        as possible. (Note that this function and :meth:`ndarray.copy` are very
        similar, but have different default values for their order=
        arguments.)
    subok : bool, optional
        If True, then sub-classes will be passed-through, otherwise the
        returned array will be forced to be a base-class array (defaults to False).

    Returns
    -------
    arr : ndarray
        Array interpretation of `a`.

    See Also
    --------
    ndarray.copy : Preferred method for creating an array copy

    Notes
    -----
    This is equivalent to:

    >>> np.array(a, copy=True)  #doctest: +SKIP

    The copy made of the data is shallow, i.e., for arrays with object dtype,
    the new array will point to the same objects.
    See Examples from `ndarray.copy`.

    Examples
    --------
    >>> import numpy as np

    Create an array x, with a reference y and a copy z:

    >>> x = np.array([1, 2, 3])
    >>> y = x
    >>> z = np.copy(x)

    Note that, when we modify x, y changes, but not z:

    >>> x[0] = 10
    >>> x[0] == y[0]
    True
    >>> x[0] == z[0]
    False

    Note that, np.copy clears previously set WRITEABLE=False flag.

    >>> a = np.array([1, 2, 3])
    >>> a.flags["WRITEABLE"] = False
    >>> b = np.copy(a)
    >>> b.flags["WRITEABLE"]
    True
    >>> b[0] = 3
    >>> b
    array([3, 2, 3])
    """
    return array(a, order=order, subok=subok, copy=True)


def copy(source: _ods_ir.Value, target: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CopyOp:
  return CopyOp(source=source, target=target, loc=loc, ip=ip)


def copy(operand: _ods_ir.Value, *, cross_program_prefetch_index: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CopyOp(operand=operand, cross_program_prefetch_index=cross_program_prefetch_index, results=results, loc=loc, ip=ip).result


def copy(a: ArrayLike, order: str | None = None) -> Array:
  """Return a copy of the array.

  JAX implementation of :func:`numpy.copy`.

  Args:
    a: arraylike object to copy
    order: not implemented in JAX

  Returns:
    a copy of the input array ``a``.

  See Also:
    - :func:`jax.numpy.array`: create an array with or without a copy.
    - :meth:`jax.Array.copy`: same function accessed as an array method.

  Examples:
    Since JAX arrays are immutable, in most cases explicit array copies
    are not necessary. One exception is when using a function with donated
    arguments (see the ``donate_argnums`` argument to :func:`jax.jit`).

    >>> f = jax.jit(lambda x: 2 * x, donate_argnums=0)
    >>> x = jnp.arange(4)
    >>> y = f(x)
    >>> print(y)
    [0 2 4 6]

    Because we marked ``x`` as being donated, the original array is no longer
    available:

    >>> print(x)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    RuntimeError: Array has been deleted with shape=int32[4].

    In situations like this, an explicit copy will let you keep access to the
    original buffer:

    >>> x = jnp.arange(4)
    >>> y = f(x.copy())
    >>> print(y)
    [0 2 4 6]
    >>> print(x)
    [0 1 2 3]
  """
  util.check_arraylike("copy", a)
  return array(a, copy=True, order=order)


def copy(
  x: FrozenDict | dict[str, Any],
  add_or_replace: FrozenDict[str, Any] | dict[str, Any] = FrozenDict({}),
) -> FrozenDict | dict[str, Any]:
  """Create a new dict with additional and/or replaced entries. This is a utility
  function that can act on either a FrozenDict or regular dict and mimics the
  behavior of ``FrozenDict.copy``.

  Example::

    >>> from flax.core import FrozenDict, copy
    >>> variables = FrozenDict({'params': {...}, 'batch_stats': {...}})
    >>> new_variables = copy(variables, {'additional_entries': 1})

  Args:
    x: the dictionary to be copied and updated
    add_or_replace: dictionary of key-value pairs to add or replace in the dict x
  Returns:
    A new dict with the additional and/or replaced entries.
  """

  if isinstance(x, FrozenDict):
    return x.copy(add_or_replace)
  elif isinstance(x, dict):
    new_dict = jax.tree_util.tree_map(
        lambda x: x, x
    )  # make a deep copy of dict x
    new_dict.update(add_or_replace)
    return new_dict
  raise TypeError(f'Expected FrozenDict or dict, got {type(x)}')


def copy(obj, byref=False, recurse=False):
    if byref:
        try:
            return dill.copy(obj, byref=byref, recurse=recurse)
        except Exception:
            pass
        else:
            raise AssertionError('Copy of %s with byref=True should have given a warning!' % (obj,))

        warnings.simplefilter('ignore')
        val = dill.copy(obj, byref=byref, recurse=recurse)
        warnings.simplefilter('error')
        return val
    else:
        return dill.copy(obj, byref=byref, recurse=recurse)

