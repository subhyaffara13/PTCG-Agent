
def _get_fields_from_model(model_class: Type[BaseModel]) -> Dict[str, Any]:
    """
    Get the fields from a Pydantic model as a nested dictionary structure
    """

    return _extract_fields_recursive(model_class, depth=0)

