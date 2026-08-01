
def catalog(request, tmp_path):
    # the catalog stores the full path of data files, so the catalog needs to be
    # created dynamically, and not saved in pandas/tests/io/data as other formats
    uri = f"sqlite:///{tmp_path}/catalog.sqlite"
    warehouse = f"file://{tmp_path}"
    catalog_name = request.param if hasattr(request, "param") else None
    catalog = pyiceberg_catalog.load_catalog(
        catalog_name or "default",
        type="sql",
        uri=uri,
        warehouse=warehouse,
    )
    catalog.create_namespace("ns")

    df = pq.read_table(
        pathlib.Path(__file__).parent / "data" / "parquet" / "simple.parquet"
    )
    table = catalog.create_table("ns.my_table", schema=df.schema)
    table.append(df)

    if catalog_name is not None:
        config_path = pathlib.Path.home() / ".pyiceberg.yaml"
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(f"""\
catalog:
  {catalog_name}:
    type: sql
    uri: {uri}
    warehouse: {warehouse}""")

        importlib.reload(pyiceberg_catalog)  # needed to reload the config file

    yield Catalog(name=catalog_name or "default", uri=uri, warehouse=warehouse)

    if catalog_name is not None:
        config_path.unlink()

