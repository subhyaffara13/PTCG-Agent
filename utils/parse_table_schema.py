
def parse_table_schema(json, precise_float: bool) -> DataFrame:
    """
    Builds a DataFrame from a given schema

    Parameters
    ----------
    json :
        A JSON table schema
    precise_float : bool
        Flag controlling precision when decoding string to double values, as
        dictated by ``read_json``

    Returns
    -------
    df : DataFrame

    Raises
    ------
    NotImplementedError
        If the JSON table schema contains either timezone or timedelta data

    Notes
    -----
        Because :func:`DataFrame.to_json` uses the string 'index' to denote a
        name-less :class:`Index`, this function sets the name of the returned
        :class:`DataFrame` to ``None`` when said string is encountered with a
        normal :class:`Index`. For a :class:`MultiIndex`, the same limitation
        applies to any strings beginning with 'level_'. Therefore, an
        :class:`Index` name of 'index'  and :class:`MultiIndex` names starting
        with 'level_' are not supported.

    See Also
    --------
    build_table_schema : Inverse function.
    pandas.read_json
    """
    table = ujson_loads(json, precise_float=precise_float)
    col_order = [field["name"] for field in table["schema"]["fields"]]
    df = DataFrame(table["data"], columns=col_order)[col_order]

    dtypes = {
        field["name"]: convert_json_field_to_pandas_type(field)
        for field in table["schema"]["fields"]
    }

    # No ISO constructor for Timedelta as of yet, so need to raise
    if "timedelta64" in dtypes.values():
        raise NotImplementedError(
            'table="orient" can not yet read ISO-formatted Timedelta data'
        )

    with option_context("future.distinguish_nan_and_na", False):
        df = df.astype(dtypes)

    if "primaryKey" in table["schema"]:
        df = df.set_index(table["schema"]["primaryKey"])
        if len(df.index.names) == 1:
            if df.index.name == "index":
                df.index.name = None
        else:
            df.index.names = [
                None if x.startswith("level_") else x for x in df.index.names
            ]

    return df

