
def get_optional_of_element_type(types):
    """Extract element type, return as `Optional[element type]` from consolidated types.

    Helper function to extracts the type of the element to be annotated to Optional
    from the list of consolidated types and returns `Optional[element type]`.
    TODO: To remove this check once Union support lands.
    """
    elem_type = types[1] if type(None) is types[0] else types[0]
    elem_type = get_type(elem_type)

    # Optional type is internally converted to Union[type, NoneType], which
    # is not supported yet in TorchScript. Hence, representing the optional type as string.
    return "Optional[" + elem_type + "]"

