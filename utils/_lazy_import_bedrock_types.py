
def _lazy_import_bedrock_types(name: str) -> Any:
    """Handler for Bedrock type aliases"""
    return _generic_lazy_import(name, _BEDROCK_TYPES_IMPORT_MAP, "Bedrock types")

