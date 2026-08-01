
def _hash_ndarray(
    vals: np.ndarray,
    encoding: str = "utf8",
    hash_key: str = _default_hash_key,
    categorize: bool = True,
) -> npt.NDArray[np.uint64]:
    """
    See hash_array.__doc__.
    """
    dtype = vals.dtype

    # _hash_ndarray only takes 64-bit values, so handle 128-bit by parts
    if np.issubdtype(dtype, np.complex128):
        hash_real = _hash_ndarray(vals.real, encoding, hash_key, categorize)
        hash_imag = _hash_ndarray(vals.imag, encoding, hash_key, categorize)
        return hash_real + 23 * hash_imag

    # First, turn whatever array this is into unsigned 64-bit ints, if we can
    # manage it.
    if dtype == bool:
        vals = vals.astype("u8")
    elif issubclass(dtype.type, (np.datetime64, np.timedelta64)):
        vals = vals.view("i8").astype("u8", copy=False)
    elif issubclass(dtype.type, np.number) and dtype.itemsize <= 8:
        vals = vals.view(f"u{vals.dtype.itemsize}").astype("u8")
    else:
        # With repeated values, its MUCH faster to categorize object dtypes,
        # then hash and rename categories. We allow skipping the categorization
        # when the values are known/likely to be unique.
        if categorize:
            from pandas import (
                Categorical,
                Index,
                factorize,
            )

            codes, categories = factorize(vals, sort=False)
            tdtype = CategoricalDtype(
                categories=Index(categories, copy=False), ordered=False
            )
            cat = Categorical._simple_new(codes, tdtype)
            return cat._hash_pandas_object(
                encoding=encoding, hash_key=hash_key, categorize=False
            )

        try:
            vals = hash_object_array(vals, hash_key, encoding)
        except TypeError:
            # we have mixed types
            vals = hash_object_array(
                vals.astype(str).astype(object), hash_key, encoding
            )

    # Then, redistribute these 64-bit ints within the space of 64-bit ints
    vals ^= vals >> 30
    vals *= np.uint64(0xBF58476D1CE4E5B9)
    vals ^= vals >> 27
    vals *= np.uint64(0x94D049BB133111EB)
    vals ^= vals >> 31
    # error: Incompatible return value type (got "Any | ndarray[tuple[int, ...],
    # dtype[signedinteger[Any]]]", expected "ndarray[tuple[int, ...],
    # dtype[unsignedinteger[_64Bit]]]")
    return vals  # type: ignore[return-value]

