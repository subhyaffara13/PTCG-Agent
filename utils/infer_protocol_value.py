
def infer_protocol_value(
    value: Any,
) -> Literal[
    "string_value",
    "number_value",
    "bool_value",
    "struct_value",
    "list_value",
    "null_value",
    "unknown",
]:
    if value is None:
        return "null_value"
    if isinstance(value, int) or isinstance(value, float):
        return "number_value"
    if isinstance(value, str):
        return "string_value"
    if isinstance(value, bool):
        return "bool_value"
    if isinstance(value, dict):
        return "struct_value"
    if isinstance(value, list):
        return "list_value"

    return "unknown"

