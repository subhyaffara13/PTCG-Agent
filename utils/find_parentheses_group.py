
def find_parentheses_group(input_string, start):
    """Finds the first balanced bracket."""
    return find_closure_group(input_string, start, group=["(", ")"])

