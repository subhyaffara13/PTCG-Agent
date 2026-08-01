
def find_bracket_group(input_string, start):
    """Finds the first balanced parentheses."""
    return find_closure_group(input_string, start, group=["{", "}"])

