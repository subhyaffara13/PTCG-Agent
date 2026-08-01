
def default_schema(schema: Any, data: Any) -> Any:
    default = get(schema, path=["default"])
    if default is None and data is None:
        return

    if get(schema, path=["type"]) == "object":
        default = deepcopy(get(default, dict, {}))
        if data is None or not has(data, dict):
            obj = default
        else:
            obj = data
            for k, v in default.items():
                if k not in obj:
                    obj[k] = v
        properties = get(schema, dict, {}, ["properties"])
        for key, prop_schema in properties.items():
            new_value = default_schema(prop_schema, get(obj, path=[key]))
            if new_value is not None:
                obj[key] = new_value
        return obj

    if get(schema, path=["type"]) == "array":
        default = deepcopy(get(default, list, []))
        arr = get(data, list, default)
        item_schema = get(schema, dict, {}, ["items"])
        for index, value in enumerate(arr):
            if value is None and len(default) > index:
                new_value = default[index]
            else:
                new_value = default_schema(item_schema, value)
            if new_value is not None:
                arr[index] = new_value
        return arr

    return data if data is not None else default

