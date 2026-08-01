
def get_fuser_method(op_list, additional_fuser_method_mapping=None):
    """Get fuser method for the given list of module types.

    Get fuser method for the given list of module types,
    return None if fuser method does not exist
    """
    if additional_fuser_method_mapping is None:
        additional_fuser_method_mapping = {}
    all_mappings = get_combined_dict(
        _DEFAULT_OP_LIST_TO_FUSER_METHOD, additional_fuser_method_mapping
    )
    fuser_method = all_mappings.get(op_list, None)
    if fuser_method is None:
        raise AssertionError(f"did not find fuser method for: {op_list} ")
    return fuser_method

