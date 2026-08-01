
def table_schema_cb(key: str) -> None:
    from pandas.io.formats.printing import enable_data_resource_formatter

    enable_data_resource_formatter(cf.get_option(key))

