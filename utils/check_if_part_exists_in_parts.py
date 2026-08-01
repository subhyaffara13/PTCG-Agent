
def check_if_part_exists_in_parts(
    parts: List[PartType], part: PartType, excluded_keys: List[str] = []
) -> bool:
    """
    Check if a part exists in a list of parts
    Handles both camelCase and snake_case key variations (e.g., function_call vs functionCall)
    """
    keys_to_compare = set(part.keys()) - set(excluded_keys)
    for p in parts:
        p_keys = set(p.keys())
        # Check if all keys in part have equivalent values in p
        match_found = True
        for key in keys_to_compare:
            equivalent_key = _get_equivalent_key(key, p_keys)
            if equivalent_key is None or p.get(equivalent_key, None) != part.get(
                key, None
            ):
                match_found = False
                break

        if match_found:
            return True
    return False

