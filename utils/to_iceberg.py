
def to_iceberg(
    df: DataFrame,
    table_identifier: str,
    catalog_name: str | None = None,
    *,
    catalog_properties: dict[str, Any] | None = None,
    location: str | None = None,
    append: bool = False,
    snapshot_properties: dict[str, str] | None = None,
) -> None:
    """
    Write a DataFrame to an Apache Iceberg table.

    .. versionadded:: 3.0.0

    Parameters
    ----------
    table_identifier : str
        Table identifier.
    catalog_name : str, optional
        The name of the catalog.
    catalog_properties : dict of {str: str}, optional
        The properties that are used next to the catalog configuration.
    location : str, optional
        Location for the table.
    append : bool, default False
        If ``True``, append data to the table, instead of replacing the content.
    snapshot_properties : dict of {str: str}, optional
        Custom properties to be added to the snapshot summary

    See Also
    --------
    read_iceberg : Read an Apache Iceberg table.
    DataFrame.to_parquet : Write a DataFrame in Parquet format.
    """
    pa = import_optional_dependency("pyarrow")
    pyiceberg_catalog = import_optional_dependency("pyiceberg.catalog")
    if catalog_properties is None:
        catalog_properties = {}
    catalog = pyiceberg_catalog.load_catalog(catalog_name, **catalog_properties)
    arrow_table = pa.Table.from_pandas(df)
    table = catalog.create_table_if_not_exists(
        identifier=table_identifier,
        schema=arrow_table.schema,
        location=location,
        # we could add `partition_spec`, `sort_order` and `properties` in the
        # future, but it may not be trivial without exposing PyIceberg objects
    )
    if snapshot_properties is None:
        snapshot_properties = {}
    if append:
        table.append(arrow_table, snapshot_properties=snapshot_properties)
    else:
        table.overwrite(arrow_table, snapshot_properties=snapshot_properties)

