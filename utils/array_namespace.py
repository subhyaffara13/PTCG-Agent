
def array_namespace(*arrays: Array, sparse_ok=False) -> ModuleType:
    """Get the array API compatible namespace for the arrays xs.

    Parameters
    ----------
    *arrays : sequence of array_like
        Arrays used to infer the common namespace.
    sparse_ok : bool
        ``True`` if `scipy.sparse` arrays should be accepted where the
        namespace would otherwise be NumPy. Default: ``False``.

    Returns
    -------
    namespace : module
        Common namespace.

    Notes
    -----
    Wrapper around `array_api_compat.array_namespace`.

    1. Check for the global switch `SCIPY_ARRAY_API`. If disabled, just
       return array_api_compat.numpy namespace and skip all compliance checks.

    2. Check for known-bad array classes.
       The following subclasses are not supported and raise and error:

       - `numpy.ma.MaskedArray`
       - `numpy.matrix`
       - NumPy arrays which do not have a boolean or numerical dtype

    3. Coerce array-likes to NumPy arrays and check their dtype.
       Note that non-scalar array-likes can't be mixed with non-NumPy Array
       API objects; e.g.

       - `array_namespace([1, 2])` returns NumPy namespace;
       - `array_namespace(np.asarray([1, 2], [3, 4])` returns NumPy namespace;
       - `array_namespace(cp.asarray([1, 2], [3, 4])` raises an error.
    """
    if not SCIPY_ARRAY_API:
        # here we could wrap the namespace if needed
        return np_compat

    numpy_arrays = []
    api_arrays = []

    for array in arrays:
        arr_info = _validate_array_cls(type(array), sparse_ok=sparse_ok)  # type:ignore[arg-type]
        if arr_info is _ArrayClsInfo.skip:
            pass

        elif arr_info is _ArrayClsInfo.numpy:
            if array.dtype.kind in 'iufcb':  # Numeric or bool
                numpy_arrays.append(array)
            elif array.dtype.kind == 'V' and is_jax_array(array):
                # Special case for JAX zero gradient arrays;
                # see array_api_compat._common._helpers._is_jax_zero_gradient_array
                api_arrays.append(array)  # JAX zero gradient array
            else:
                raise TypeError(f"An argument has dtype `{array.dtype!r}`; "
                                "only boolean and numerical dtypes are supported.")

        elif arr_info is _ArrayClsInfo.unknown and is_array_api_obj(array):
            api_arrays.append(array)

        else:
            # list, tuple, or arbitrary object
            try:
                array = np.asanyarray(array)
            except TypeError:
                raise TypeError("An argument is neither array API compatible nor "
                                "coercible by NumPy.")
            if array.dtype.kind not in 'iufcb':  # Numeric or bool
                raise TypeError(f"An argument has dtype `{array.dtype!r}`; "
                                "only boolean and numerical dtypes are supported.")
            numpy_arrays.append(array)

    # When there are exclusively NumPy and ArrayLikes, skip calling
    # array_api_compat.array_namespace for performance.
    if not api_arrays:
        return np_compat

    # In case of mix of NumPy/ArrayLike and non-NumPy Array API arrays,
    # let array_api_compat.array_namespace raise an error.
    return array_api_compat.array_namespace(*numpy_arrays, *api_arrays)


def array_namespace(
    *xs: Array | complex | None,
    api_version: str | None = None,
    use_compat: bool | None = None,
) -> Namespace:
    """
    Get the array API compatible namespace for the arrays `xs`.

    Parameters
    ----------
    xs: arrays
        one or more arrays. xs can also be Python scalars (bool, int, float,
        complex, or None), which are ignored.

    api_version: str
        The newest version of the spec that you need support for (currently
        the compat library wrapped APIs support v2025.12).

    use_compat: bool or None
        If None (the default), the native namespace will be returned if it is
        already array API compatible; otherwise, a compat wrapper is used. If
        True, the compat library wrapped library will be returned. If False,
        the native library namespace is returned.

    Returns
    -------

    out: namespace
        The array API compatible namespace corresponding to the arrays in `xs`.

    Raises
    ------
    TypeError
        If `xs` contains arrays from different array libraries or contains a
        non-array.


    Typical usage is to pass the arguments of a function to
    `array_namespace()` at the top of a function to get the corresponding
    array API namespace:

    .. code:: python

       def your_function(x, y):
           xp = array_api_compat.array_namespace(x, y)
           # Now use xp as the array library namespace
           return xp.mean(x, axis=0) + 2*xp.std(y, axis=0)


    Wrapped array namespaces can also be imported directly. For example,
    `array_namespace(np.array(...))` will return `array_api_compat.numpy`.
    This function will also work for any array library not wrapped by
    array-api-compat if it explicitly defines `__array_namespace__
    <https://data-apis.org/array-api/latest/API_specification/generated/array_api.array.__array_namespace__.html>`__
    (the wrapped namespace is always preferred if it exists).

    See Also
    --------

    is_array_api_obj
    is_numpy_array
    is_cupy_array
    is_torch_array
    is_dask_array
    is_jax_array
    is_pydata_sparse_array

    """
    namespaces: set[Namespace] = set()
    for x in xs:
        xp, info = _cls_to_namespace(cast(Hashable, type(x)), api_version, use_compat)
        if info is _ClsToXPInfo.SCALAR:
            continue

        if (
            info is _ClsToXPInfo.MAYBE_JAX_ZERO_GRADIENT
            and _is_jax_zero_gradient_array(x)
        ):
            xp = _jax_namespace(api_version, use_compat)

        if xp is None:
            get_ns = getattr(x, "__array_namespace__", None)
            if get_ns is None:
                raise TypeError(f"{type(x).__name__} is not a supported array type")
            if use_compat:
                raise ValueError(
                    "The given array does not have an array-api-compat wrapper"
                )
            xp = get_ns(api_version=api_version)

        namespaces.add(xp)

    try:
        (xp,) = namespaces
        return xp
    except ValueError:
        if not namespaces:
            raise TypeError(
                "array_namespace requires at least one non-scalar array input"
            )
        raise TypeError(f"Multiple namespaces for array inputs: {namespaces}")

