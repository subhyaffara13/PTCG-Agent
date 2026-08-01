
def convert_pandas_type_to_json_field(arr) -> dict[str, JSONSerializable]:
    dtype = arr.dtype
    name: JSONSerializable
    if arr.name is None:
        name = "values"
    else:
        name = arr.name
    field: dict[str, JSONSerializable] = {
        "name": name,
        "type": as_json_table_type(dtype),
    }

    if isinstance(dtype, CategoricalDtype):
        cats = dtype.categories
        ordered = dtype.ordered

        field["constraints"] = {"enum": list(cats)}
        field["ordered"] = ordered
    elif isinstance(dtype, PeriodDtype):
        field["freq"] = dtype.freq.freqstr
    elif isinstance(dtype, DatetimeTZDtype):
        if timezones.is_utc(dtype.tz):
            field["tz"] = "UTC"
        else:
            zone = timezones.get_timezone(dtype.tz)
            if isinstance(zone, str):
                field["tz"] = zone
    elif isinstance(dtype, ExtensionDtype):
        field["extDtype"] = dtype.name
    return field

