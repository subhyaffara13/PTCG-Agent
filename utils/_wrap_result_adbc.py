
def _wrap_result_adbc(
    df: DataFrame,
    *,
    index_col=None,
    parse_dates=None,
    dtype: DtypeArg | None = None,
    dtype_backend: DtypeBackend | Literal["numpy"] = "numpy",
) -> DataFrame:
    """Wrap result set of a SQLAlchemy query in a DataFrame."""
    if dtype:
        df = df.astype(dtype)

    df = _parse_date_columns(df, parse_dates)

    if index_col is not None:
        df = df.set_index(index_col)

    return df

