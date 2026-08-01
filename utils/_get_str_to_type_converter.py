
def _get_str_to_type_converter(setting_name: str) -> Callable[[str], Any] | type[Any]:
    type_converter: Callable[[str], Any] | type[Any] = type(_DEFAULT_SETTINGS.get(setting_name, ""))
    if type_converter == WrapModes:
        type_converter = wrap_mode_from_string
    return type_converter

