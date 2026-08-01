
def asarray_tuplesafe(
    values: ArrayLike | list | tuple | zip, dtype: NpDtype | None = ...
) -> np.ndarray:
    # ExtensionArray can only be returned when values is an Index, all other iterables
    # will return np.ndarray. Unfortunately "all other" cannot be encoded in a type
    # signature, so instead we special-case some common types.
    ...


def asarray_tuplesafe(values: Iterable, dtype: NpDtype | None = ...) -> ArrayLike: ...


def asarray_tuplesafe(values: Iterable, dtype: NpDtype | None = None) -> ArrayLike:
    if not (isinstance(values, (list, tuple)) or hasattr(values, "__array__")):
        values = list(values)
    elif isinstance(values, ABCIndex):
        return values._values
    elif isinstance(values, ABCSeries):
        return values._values

    if isinstance(values, list) and dtype in [np.object_, object]:
        return construct_1d_object_array_from_listlike(values)

    try:
        result = np.asarray(values, dtype=dtype)
    except ValueError:
        # Using try/except since it's more performant than checking is_list_like
        # over each element
        # error: Argument 1 to "construct_1d_object_array_from_listlike"
        # has incompatible type "Iterable[Any]"; expected "Sized"
        return construct_1d_object_array_from_listlike(values)  # type: ignore[arg-type]

    if issubclass(result.dtype.type, str):
        result = np.asarray(values, dtype=object)

    if result.ndim == 2:
        # Avoid building an array of arrays:
        values = [tuple(x) for x in values]
        result = construct_1d_object_array_from_listlike(values)

    return result

