
def concat_codes(list_of_codes: list[cpy.CodeArray]) -> cpy.CodeArray:
    """Concatenate a list of codes arrays into a single code array.
    """
    if not list_of_codes:
        raise ValueError("Empty list passed to concat_codes")

    return np.concatenate(list_of_codes, dtype=code_dtype)

