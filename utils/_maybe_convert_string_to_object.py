
def _maybe_convert_string_to_object(
    data: pd.Series | pd.Index,
) -> pd.Series | pd.Index | None:
    if isinstance(data.dtype, pd.StringDtype) and data.dtype.na_value is np.nan:
        return data.astype("object").fillna(None)
    elif isinstance(data.dtype, pd.CategoricalDtype):
        cat_dtype = data.dtype.categories.dtype
        if isinstance(cat_dtype, pd.StringDtype) and cat_dtype.na_value is np.nan:
            cat_dtype = pd.CategoricalDtype(
                categories=data.dtype.categories.astype("object"),
                ordered=data.dtype.ordered,
            )
            return data.astype(cat_dtype)

    # no conversion needed
    return None

