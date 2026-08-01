
def invalidate_string_dtypes(dtype_set: set[DtypeObj]) -> None:
    """
    Change string like dtypes to object for
    ``DataFrame.select_dtypes()``.
    """
    # error: Argument 1 to <set> has incompatible type "Type[generic]"; expected
    # "Union[dtype[Any], ExtensionDtype, None]"
    # error: Argument 2 to <set> has incompatible type "Type[generic]"; expected
    # "Union[dtype[Any], ExtensionDtype, None]"
    non_string_dtypes = dtype_set - {
        np.dtype("S").type,  # type: ignore[arg-type]
        np.dtype("<U").type,  # type: ignore[arg-type]
    }
    if non_string_dtypes != dtype_set:
        raise TypeError(
            "numpy string dtypes are not allowed, use 'str' or 'object' instead"
        )

