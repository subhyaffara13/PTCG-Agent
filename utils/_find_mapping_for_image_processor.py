
def _find_mapping_for_image_processor(base_class_name: str) -> dict | None:
    """
    Find the backend->class mapping that contains base_class_name in its values.
    Returns the mapping dict (including any custom registered backends) or None.
    """

    def _value_matches(val, name: str) -> bool:
        if val is None:
            return False
        if isinstance(val, str):
            return val == name
        if isinstance(val, type):
            return getattr(val, "__name__", None) == name
        return False

    for mapping_dict in IMAGE_PROCESSOR_MAPPING_NAMES.values():
        if any(_value_matches(v, base_class_name) for v in mapping_dict.values()):
            return mapping_dict

    for content in IMAGE_PROCESSOR_MAPPING._extra_content.values():
        if any(_value_matches(v, base_class_name) for v in content.values()):
            return content

    return None

