
def treat_as_nested(data) -> bool:
    """
    Check if we should use nested_data_to_arrays.
    """
    return (
        len(data) > 0
        and is_list_like(data[0])
        and getattr(data[0], "ndim", 1) == 1
        and not (isinstance(data, ExtensionArray) and data.ndim == 2)
    )

