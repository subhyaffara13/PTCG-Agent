
def _get_dict_key_options(field_annotation: Any) -> Optional[List[str]]:
    """
    Extract key options from Dict[Literal[...], T] types
    """
    if (
        hasattr(field_annotation, "__origin__")
        and field_annotation.__origin__ is dict
        and hasattr(field_annotation, "__args__")
    ):
        args = field_annotation.__args__
        if len(args) >= 2:
            key_type = args[0]
            return _extract_literal_values(key_type)
    return None

