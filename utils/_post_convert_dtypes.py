
def _post_convert_dtypes(
    df: pd.DataFrame,
    dtype_backend: DtypeBackend | Literal["numpy"] | lib.NoDefault,
    dtype: DtypeArg | None,
    names: Sequence[Hashable] | None,
) -> pd.DataFrame:
    if dtype is not None and (
        dtype_backend is lib.no_default or dtype_backend == "numpy"
    ):
        # GH#56136 apply any user-provided dtype, and convert any IntegerDtype
        #  columns the user didn't explicitly ask for.
        if isinstance(dtype, dict):
            if names is not None:
                df.columns = names

            cmp_dtypes = {
                pd.Int8Dtype(),
                pd.Int16Dtype(),
                pd.Int32Dtype(),
                pd.Int64Dtype(),
            }
            for col in df.columns:
                if col not in dtype and df[col].dtype in cmp_dtypes:
                    # Any key that the user didn't explicitly specify
                    #  that got converted to IntegerDtype now gets converted
                    #  to numpy dtype.
                    dtype[col] = df[col].dtype.numpy_dtype

            # Ignore non-existent columns from dtype mapping
            # like other parsers do
            dtype = {
                key: pandas_dtype(dtype[key]) for key in dtype if key in df.columns
            }

        else:
            dtype = pandas_dtype(dtype)

        try:
            df = df.astype(dtype)
        except TypeError as err:
            # GH#44901 reraise to keep api consistent
            raise ValueError(str(err)) from err

    if (
        not using_string_dtype()
        and dtype != "str"
        and (dtype_backend is lib.no_default or dtype_backend == "numpy")
    ):
        # Convert any StringDtype columns back to object dtype (pyarrow always
        # uses string dtype even when the infer_string option is False)
        for i in range(len(df.columns)):
            new_col = _maybe_convert_string_to_object(df.iloc[:, i])
            if new_col is not None:
                df.isetitem(i, new_col)

        new_idx = _maybe_convert_string_index_to_object(df.index)
        if new_idx is not None:
            df.index = new_idx
        new_cols = _maybe_convert_string_index_to_object(df.columns)
        if new_cols is not None:
            df.columns = new_cols

    return df

