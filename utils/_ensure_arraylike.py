
def _ensure_arraylike(values, func_name: str) -> ArrayLike:
    """
    ensure that we are arraylike if not already
    """
    if not isinstance(
        values,
        (ABCIndex, ABCSeries, ABCExtensionArray, np.ndarray, ABCNumpyExtensionArray),
    ):
        # GH#52986
        if func_name != "isin-targets":
            # Make an exception for the comps argument in isin.
            raise TypeError(
                f"{func_name} requires a Series, Index, "
                f"ExtensionArray, np.ndarray or NumpyExtensionArray "
                f"got {type(values).__name__}."
            )

        inferred = lib.infer_dtype(values, skipna=False)
        if inferred in ["mixed", "string", "mixed-integer"]:
            # "mixed-integer" to ensure we do not cast ["ss", 42] to str GH#22160
            if isinstance(values, tuple):
                values = list(values)
            values = construct_1d_object_array_from_listlike(values)
        else:
            values = np.asarray(values)
    return values

