
def result_type(*arrays_and_dtypes):
    tensors = []
    for entry in arrays_and_dtypes:
        try:
            t = asarray(entry).tensor
        except (RuntimeError, ValueError, TypeError):
            dty = _dtypes.dtype(entry)
            t = torch.empty(1, dtype=dty.torch_dtype)
        tensors.append(t)

    torch_dtype = _dtypes_impl.result_type_impl(*tensors)
    return _dtypes.dtype(torch_dtype)


def result_type(*arrays_and_dtypes: Array | DType | complex) -> DType:
    num = len(arrays_and_dtypes)

    if num == 0:
        raise ValueError("At least one array or dtype must be provided")

    elif num == 1:
        x = arrays_and_dtypes[0]
        if isinstance(x, torch.dtype):
            return x
        return x.dtype

    if num == 2:
        x, y = arrays_and_dtypes
        return _result_type(x, y)

    else:
        # sort scalars so that they are treated last
        scalars, others = [], []
        for x in arrays_and_dtypes:
            if isinstance(x, _py_scalars):
                scalars.append(x)
            else:
                others.append(x)
        if not others:
            raise ValueError("At least one array or dtype must be provided")

        # combine left-to-right
        return _reduce(_result_type, others + scalars)


def result_type(*arrays_and_dtypes):
    """
    result_type(*arrays_and_dtypes)

    Returns the type that results from applying the NumPy
    :ref:`type promotion <arrays.promotion>` rules to the arguments.

    Parameters
    ----------
    arrays_and_dtypes : list of arrays and dtypes
        The operands of some operation whose result type is needed.

    Returns
    -------
    out : dtype
        The result type.

    See also
    --------
    dtype, promote_types, min_scalar_type, can_cast

    Examples
    --------
    >>> import numpy as np
    >>> np.result_type(3, np.arange(7, dtype=np.int8))
    dtype('int8')

    >>> np.result_type(np.int32, np.complex64)
    dtype('complex128')

    >>> np.result_type(3.0, -2)
    dtype('float64')

    """
    return arrays_and_dtypes


def result_type(*args: Any, return_weak_type_flag: Literal[True]) -> tuple[DType, bool]: ...


def result_type(*args: Any, return_weak_type_flag: Literal[False] = False) -> DType: ...


def result_type(*args: Any, return_weak_type_flag: bool = False) -> DType | tuple[DType, bool]: ...


def result_type(*args: Any, return_weak_type_flag: bool = False) -> DType | tuple[DType, bool]:
  """Convenience function to apply JAX argument dtype promotion.

  Args:
    return_weak_type_flag : if True, then return a ``(dtype, weak_type)`` tuple.
      If False, just return `dtype`

  Returns:
    dtype or (dtype, weak_type) depending on the value of the ``return_weak_type`` argument.
  """
  if len(args) == 0:
    raise ValueError("at least one array or dtype is required")
  dtype: DType | ExtendedDType
  dtype, weak_type = lattice_result_type(*(default_float_dtype() if arg is None else arg for arg in args))
  if weak_type:
    dtype = default_types['f' if dtype in _custom_float_dtypes else dtype.kind]()
  return (dtype, weak_type) if return_weak_type_flag else dtype


def result_type(*args: Any) -> DType:
  """Return the result of applying JAX promotion rules to the inputs.

  JAX implementation of :func:`numpy.result_type`.

  JAX's dtype promotion behavior is described in :ref:`type-promotion`.

  Args:
    args: one or more arrays or dtype-like objects.

  Returns:
    A :class:`numpy.dtype` instance representing the result of type
    promotion for the inputs.

  Examples:
    Inputs can be dtype specifiers:

    >>> jnp.result_type('int32', 'float32')
    dtype('float32')
    >>> jnp.result_type(np.uint16, np.dtype('int32'))
    dtype('int32')

    Inputs may also be scalars or arrays:

    >>> jnp.result_type(1.0, jnp.bfloat16(2))
    dtype(bfloat16)
    >>> jnp.result_type(jnp.arange(4), jnp.zeros(4))
    dtype('float32')

    Be aware that the result type will be canonicalized based on the state
    of the ``jax_enable_x64`` configuration flag, meaning that 64-bit types
    may be downcast to 32-bit:

    >>> jnp.result_type('float64')  # doctest: +SKIP
    dtype('float32')

    For details on 64-bit values, refer to `Sharp bits - double precision`_:

    .. _Sharp bits - double precision: https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html#double-64bit-precision
  """
  return dtypes.result_type(*args)

