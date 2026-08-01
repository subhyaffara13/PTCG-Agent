
def _json_dict_factory(data: list[tuple[str, Any]]) -> dict[str, Any]:
    return {key: value for key, value in data if value is not None}


def _json_dict_factory(data: list[tuple[str, Any]]) -> dict[str, Any]:
    return {key: value for key, value in data if value is not None}

