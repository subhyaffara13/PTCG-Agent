
def _process_parameter_type(param):
    """
    Process and format a parameter's type annotation from an inspect.Parameter object.

    Args:
        param (`inspect.Parameter`): The parameter from the function signature

    Returns:
        tuple[str, bool]: (formatted_type_string, is_optional)
    """
    if param.annotation == inspect.Parameter.empty:
        return "", False

    # Use the unified function to process the type annotation
    formatted_type, optional = process_type_annotation(param.annotation)

    # Check if parameter has a default value (makes it optional)
    if param.default is not inspect.Parameter.empty:
        optional = True

    return formatted_type, optional

