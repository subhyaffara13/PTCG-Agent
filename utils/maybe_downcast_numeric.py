
def maybe_downcast_numeric(
    result: np.ndarray, dtype: np.dtype, do_round: bool = False
) -> np.ndarray: ...


def maybe_downcast_numeric(
    result: ExtensionArray, dtype: DtypeObj, do_round: bool = False
) -> ArrayLike: ...


def maybe_downcast_numeric(
    result: ArrayLike, dtype: DtypeObj, do_round: bool = False
) -> ArrayLike:
    """
    Subset of maybe_downcast_to_dtype restricted to numeric dtypes.

    Parameters
    ----------
    result : ndarray or ExtensionArray
    dtype : np.dtype or ExtensionDtype
    do_round : bool

    Returns
    -------
    ndarray or ExtensionArray
    """
    if not isinstance(dtype, np.dtype) or not isinstance(result.dtype, np.dtype):
        # e.g. SparseDtype has no itemsize attr
        return result

    def trans(x):
        if do_round:
            return x.round()
        return x

    if dtype.kind == result.dtype.kind:
        # don't allow upcasts here (except if empty)
        if result.dtype.itemsize <= dtype.itemsize and result.size:
            return result

    if dtype.kind in "biu":
        if not result.size:
            # if we don't have any elements, just astype it
            return trans(result).astype(dtype)

        if isinstance(result, np.ndarray):
            element = result.item(0)
        else:
            element = result.iloc[0]
        if not isinstance(element, (np.integer, np.floating, int, float, bool)):
            # a comparable, e.g. a Decimal may slip in here
            return result

        if (
            issubclass(result.dtype.type, (np.object_, np.number))
            and notna(result).all()
        ):
            new_result = trans(result).astype(dtype)
            if new_result.dtype.kind == "O" or result.dtype.kind == "O":
                # np.allclose may raise TypeError on object-dtype
                if (new_result == result).all():
                    return new_result
            elif np.allclose(new_result, result, rtol=0):
                return new_result

    elif (
        issubclass(dtype.type, np.floating)
        and result.dtype.kind != "b"
        and not is_string_dtype(result.dtype)
    ):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", "overflow encountered in cast", RuntimeWarning
            )
            new_result = result.astype(dtype)

        # Adjust tolerances based on floating point size
        size_tols = {4: 5e-4, 8: 5e-8, 16: 5e-16}

        atol = size_tols.get(new_result.dtype.itemsize, 0.0)

        # Check downcast float values are still equal within 7 digits when
        # converting from float64 to float32
        if np.allclose(new_result, result, equal_nan=True, rtol=0.0, atol=atol):
            return new_result

    elif dtype.kind == result.dtype.kind == "c":
        new_result = result.astype(dtype)

        if np.array_equal(new_result, result, equal_nan=True):
            # TODO: use tolerance like we do for float?
            return new_result

    return result

