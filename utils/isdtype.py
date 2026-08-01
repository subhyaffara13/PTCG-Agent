
def isdtype(
    dtype: DType,
    kind: DType | str | tuple[DType | str, ...],
    xp: Namespace,
    *,
    _tuple: bool = True,  # Disallow nested tuples
) -> bool:
    """
    Returns a boolean indicating whether a provided dtype is of a specified data type ``kind``.

    Note that outside of this function, this compat library does not yet fully
    support complex numbers.

    See
    https://data-apis.org/array-api/latest/API_specification/generated/array_api.isdtype.html
    for more details
    """
    if isinstance(kind, tuple) and _tuple:
        return any(
            isdtype(dtype, k, xp, _tuple=False)
            for k in cast("tuple[DType | str, ...]", kind)
        )
    elif isinstance(kind, str):
        if kind == "bool":
            return dtype == xp.bool_
        elif kind == "signed integer":
            return xp.issubdtype(dtype, xp.signedinteger)
        elif kind == "unsigned integer":
            return xp.issubdtype(dtype, xp.unsignedinteger)
        elif kind == "integral":
            return xp.issubdtype(dtype, xp.integer)
        elif kind == "real floating":
            return xp.issubdtype(dtype, xp.floating)
        elif kind == "complex floating":
            return xp.issubdtype(dtype, xp.complexfloating)
        elif kind == "numeric":
            return xp.issubdtype(dtype, xp.number)
        else:
            raise ValueError(f"Unrecognized data type kind: {kind!r}")
    else:
        # This will allow things that aren't required by the spec, like
        # isdtype(np.float64, float) or isdtype(np.int64, 'l'). Should we be
        # more strict here to match the type annotation? Note that the
        # array_api_strict implementation will be very strict.
        return dtype == kind


def isdtype(
    dtype: DType, 
    kind: DType | str | tuple[DType | str, ...],
    *,
    _tuple: bool = True, # Disallow nested tuples
) -> bool:
    """
    Returns a boolean indicating whether a provided dtype is of a specified data type ``kind``.

    Note that outside of this function, this compat library does not yet fully
    support complex numbers.

    See
    https://data-apis.org/array-api/latest/API_specification/generated/array_api.isdtype.html
    for more details
    """
    if isinstance(kind, tuple) and _tuple:
        return _builtin_any(isdtype(dtype, k, _tuple=False) for k in kind)
    elif isinstance(kind, str):
        if kind == 'bool':
            return dtype == torch.bool
        elif kind == 'signed integer':
            return dtype in _int_dtypes and dtype.is_signed
        elif kind == 'unsigned integer':
            return dtype in _int_dtypes and not dtype.is_signed
        elif kind == 'integral':
            return dtype in _int_dtypes
        elif kind == 'real floating':
            return dtype.is_floating_point
        elif kind == 'complex floating':
            return dtype.is_complex
        elif kind == 'numeric':
            return isdtype(dtype, ('integral', 'real floating', 'complex floating'))
        else:
            raise ValueError(f"Unrecognized data type kind: {kind!r}")
    else:
        return dtype == kind


def isdtype(dtype, kind):
    """
    Determine if a provided dtype is of a specified data type ``kind``.

    This function only supports built-in NumPy's data types.
    Third-party dtypes are not yet supported.

    Parameters
    ----------
    dtype : dtype
        The input dtype.
    kind : dtype or str or tuple of dtypes/strs.
        dtype or dtype kind. Allowed dtype kinds are:
        * ``'bool'`` : boolean kind
        * ``'signed integer'`` : signed integer data types
        * ``'unsigned integer'`` : unsigned integer data types
        * ``'integral'`` : integer data types
        * ``'real floating'`` : real-valued floating-point data types
        * ``'complex floating'`` : complex floating-point data types
        * ``'numeric'`` : numeric data types

    Returns
    -------
    out : bool

    See Also
    --------
    issubdtype

    Examples
    --------
    >>> import numpy as np
    >>> np.isdtype(np.float32, np.float64)
    False
    >>> np.isdtype(np.float32, "real floating")
    True
    >>> np.isdtype(np.complex128, ("real floating", "complex floating"))
    True

    """
    try:
        dtype = _preprocess_dtype(dtype)
    except _PreprocessDTypeError:
        raise TypeError(
            "dtype argument must be a NumPy dtype, "
            f"but it is a {type(dtype)}."
        ) from None

    input_kinds = kind if isinstance(kind, tuple) else (kind,)

    processed_kinds = set()

    for kind in input_kinds:
        if kind == "bool":
            processed_kinds.add(allTypes["bool"])
        elif kind == "signed integer":
            processed_kinds.update(sctypes["int"])
        elif kind == "unsigned integer":
            processed_kinds.update(sctypes["uint"])
        elif kind == "integral":
            processed_kinds.update(sctypes["int"] + sctypes["uint"])
        elif kind == "real floating":
            processed_kinds.update(sctypes["float"])
        elif kind == "complex floating":
            processed_kinds.update(sctypes["complex"])
        elif kind == "numeric":
            processed_kinds.update(
                sctypes["int"] + sctypes["uint"] +
                sctypes["float"] + sctypes["complex"]
            )
        elif isinstance(kind, str):
            raise ValueError(
                "kind argument is a string, but"
                f" {kind!r} is not a known kind name."
            )
        else:
            try:
                kind = _preprocess_dtype(kind)
            except _PreprocessDTypeError:
                raise TypeError(
                    "kind argument must be comprised of "
                    "NumPy dtypes or strings only, "
                    f"but is a {type(kind)}."
                ) from None
            processed_kinds.add(kind)

    return dtype in processed_kinds


def isdtype(dtype: DTypeLike, kind: str | DTypeLike | tuple[str | DTypeLike, ...]) -> bool:
  """Returns a boolean indicating whether a provided dtype is of a specified kind.

  Args:
    dtype : the input dtype
    kind : the data type kind.
      If ``kind`` is dtype-like, return ``dtype = kind``.
      If ``kind`` is a string, then return True if the dtype is in the specified category:

      - ``'bool'``: ``{bool}``
      - ``'signed integer'``: ``{int4, int8, int16, int32, int64}``
      - ``'unsigned integer'``: ``{uint4, uint8, uint16, uint32, uint64}``
      - ``'integral'``: shorthand for ``('signed integer', 'unsigned integer')``
      - ``'real floating'``: ``{float8_*, float16, bfloat16, float32, float64}``
      - ``'complex floating'``: ``{complex64, complex128}``
      - ``'numeric'``: shorthand for ``('integral', 'real floating', 'complex floating')``

      If ``kind`` is a tuple, then return True if dtype matches any entry of the tuple.

  Returns:
    True or False
  """
  the_dtype = np.dtype(dtype)
  kind_tuple: tuple[str | DTypeLike, ...] = (
    kind if isinstance(kind, tuple) else (kind,)
  )
  options: set[DType] = set()
  for kind in kind_tuple:
    if isinstance(kind, str) and kind in _dtype_kinds:
      options.update(_dtype_kinds[kind])
      continue
    try:
      _dtype = np.dtype(kind)
    except TypeError as e:
      if isinstance(kind, str):
        raise ValueError(
          f"Unrecognized {kind=} expected one of {list(_dtype_kinds.keys())}, "
          "or a compatible input for jnp.dtype()")
      raise TypeError(
        f"Expected kind to be a dtype, string, or tuple; got {kind=}"
      ) from e
    options.add(_dtype)
  return the_dtype in options

