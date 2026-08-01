
def dtype_backend_expected():
    def func(string_storage, dtype_backend, conn_name) -> DataFrame:
        string_dtype: pd.StringDtype | pd.ArrowDtype
        if dtype_backend == "pyarrow":
            pa = pytest.importorskip("pyarrow")
            string_dtype = pd.ArrowDtype(pa.string())
        else:
            string_dtype = pd.StringDtype(string_storage)

        df = DataFrame(
            {
                "a": Series([1, pd.NA, 3], dtype="Int64"),
                "b": Series([1, 2, 3], dtype="Int64"),
                "c": Series([1.5, pd.NA, 2.5], dtype="Float64"),
                "d": Series([1.5, 2.0, 2.5], dtype="Float64"),
                "e": Series([True, False, pd.NA], dtype="boolean"),
                "f": Series([True, False, True], dtype="boolean"),
                "g": Series(["a", "b", "c"], dtype=string_dtype),
                "h": Series(["a", "b", None], dtype=string_dtype),
            }
        )
        if dtype_backend == "pyarrow":
            pa = pytest.importorskip("pyarrow")

            from pandas.arrays import ArrowExtensionArray

            df = DataFrame(
                {
                    col: ArrowExtensionArray(pa.array(df[col], from_pandas=True))
                    for col in df.columns
                }
            )

        if "mysql" in conn_name or "sqlite" in conn_name:
            if dtype_backend == "numpy_nullable":
                df = df.astype({"e": "Int64", "f": "Int64"})
            else:
                df = df.astype({"e": "int64[pyarrow]", "f": "int64[pyarrow]"})

        return df

    return func

