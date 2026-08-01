
def from_dataframe(df, allow_copy: bool = True) -> pd.DataFrame:
    """
    Build a ``pd.DataFrame`` from any DataFrame supporting the interchange protocol.

    .. note::

       For new development, we highly recommend using the Arrow C Data Interface
       alongside the Arrow PyCapsule Interface instead of the interchange protocol.
       From pandas 3.0 onwards, `from_dataframe` uses the PyCapsule Interface,
       only falling back to the interchange protocol if that fails.

       From pandas 4.0 onwards, that fallback will no longer be available and only
       the PyCapsule Interface will be used.

    .. warning::

        Due to severe implementation issues, we recommend only considering using the
        interchange protocol in the following cases:

        - converting to pandas: for pandas >= 2.0.3
        - converting from pandas: for pandas >= 3.0.0

    Parameters
    ----------
    df : DataFrameXchg
        Object supporting the interchange protocol, i.e. `__dataframe__` method.
    allow_copy : bool, default: True
        Whether to allow copying the memory to perform the conversion
        (if false then zero-copy approach is requested).

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame built from the provided interchange
        protocol object.

    See Also
    --------
    pd.DataFrame : DataFrame class which can be created from various input data
        formats, including objects that support the interchange protocol.

    Examples
    --------
    >>> df_not_necessarily_pandas = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    >>> interchange_object = df_not_necessarily_pandas.__dataframe__()
    >>> interchange_object.column_names()
    Index(['A', 'B'], dtype='str')
    >>> df_pandas = pd.api.interchange.from_dataframe(
    ...     interchange_object.select_columns_by_name(["A"])
    ... )
    >>> df_pandas
         A
    0    1
    1    2

    These methods (``column_names``, ``select_columns_by_name``) should work
    for any dataframe library which implements the interchange protocol.
    """
    if isinstance(df, pd.DataFrame):
        return df

    if hasattr(df, "__arrow_c_stream__"):
        try:
            pa = import_optional_dependency("pyarrow", min_version="14.0.0")
        except ImportError:
            # fallback to _from_dataframe
            warnings.warn(
                "Conversion using Arrow PyCapsule Interface failed due to "
                "missing PyArrow>=14 dependency, falling back to (deprecated) "
                "interchange protocol. We recommend that you install "
                "PyArrow>=14.0.0.",
                UserWarning,
                stacklevel=find_stack_level(),
            )
        else:
            try:
                return pa.table(df).to_pandas(zero_copy_only=not allow_copy)
            except pa.ArrowInvalid as e:
                raise RuntimeError(e) from e

    if not hasattr(df, "__dataframe__"):
        raise ValueError("`df` does not support __dataframe__")

    warnings.warn(
        "The Dataframe Interchange Protocol is deprecated.\n"
        "For dataframe-agnostic code, you may want to look into:\n"
        "- Arrow PyCapsule Interface: https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html\n"
        "- Narwhals: https://github.com/narwhals-dev/narwhals\n",
        Pandas4Warning,
        stacklevel=find_stack_level(),
    )

    return _from_dataframe(
        df.__dataframe__(allow_copy=allow_copy), allow_copy=allow_copy
    )

