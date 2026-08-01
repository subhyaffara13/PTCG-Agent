
def backend(request):
    if request.param == "numpy":

        def make_dataframe(*args, **kwargs):
            return DataFrame(*args, **kwargs)

        def make_series(*args, **kwargs):
            return Series(*args, **kwargs)

    elif request.param == "nullable":

        def make_dataframe(*args, **kwargs):
            df = DataFrame(*args, **kwargs)
            df_nullable = df.convert_dtypes()
            # convert_dtypes will try to cast float to int if there is no loss in
            # precision -> undo that change
            for col in df.columns:
                if is_float_dtype(df[col].dtype) and not is_float_dtype(
                    df_nullable[col].dtype
                ):
                    df_nullable[col] = df_nullable[col].astype("Float64")
            # copy final result to ensure we start with a fully self-owning DataFrame
            return df_nullable.copy()

        def make_series(*args, **kwargs):
            ser = Series(*args, **kwargs)
            return ser.convert_dtypes().copy()

    return request.param, make_dataframe, make_series

