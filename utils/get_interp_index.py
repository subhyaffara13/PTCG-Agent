
def get_interp_index(method, index: Index) -> Index:
    # create/use the index
    if method == "linear":
        # prior default
        from pandas import RangeIndex

        index = RangeIndex(len(index))
    else:
        methods = {"index", "values", "nearest", "time"}
        is_numeric_or_datetime = (
            is_numeric_dtype(index.dtype)
            or isinstance(index.dtype, DatetimeTZDtype)
            or lib.is_np_dtype(index.dtype, "mM")
        )
        valid = NP_METHODS + SP_METHODS
        if method in valid:
            if method not in methods and not is_numeric_or_datetime:
                raise ValueError(
                    "Index column must be numeric or datetime type when "
                    f"using {method} method other than linear. "
                    "Try setting a numeric or datetime index column before "
                    "interpolating."
                )
        else:
            raise ValueError(f"Can not interpolate with method={method}.")

    if isna(index).any():
        raise NotImplementedError(
            "Interpolation with NaNs in the index "
            "has not been implemented. Try filling "
            "those NaNs before interpolating."
        )
    return index

