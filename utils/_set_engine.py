
def _set_engine(engine_str):
    # Define a list of parquet engines to try
    if engine_str == "auto":
        try_engines = ("fastparquet", "pyarrow")
    elif not isinstance(engine_str, str):
        raise ValueError(
            "Failed to set parquet engine! "
            "Please pass 'fastparquet', 'pyarrow', or 'auto'"
        )
    elif engine_str not in ("fastparquet", "pyarrow"):
        raise ValueError(f"{engine_str} engine not supported by `fsspec.parquet`")
    else:
        try_engines = [engine_str]

    # Try importing the engines in `try_engines`,
    # and choose the first one that succeeds
    for engine in try_engines:
        try:
            if engine == "fastparquet":
                return FastparquetEngine()
            elif engine == "pyarrow":
                return PyarrowEngine()
        except ImportError:
            pass

    # Raise an error if a supported parquet engine
    # was not found
    raise ImportError(
        f"The following parquet engines are not installed "
        f"in your python environment: {try_engines}."
        f"Please install 'fastparquert' or 'pyarrow' to "
        f"utilize the `fsspec.parquet` module."
    )

