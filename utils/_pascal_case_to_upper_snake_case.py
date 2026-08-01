
def _pascal_case_to_upper_snake_case(string):
    return _pascal_to_upper_snake_case_regex.sub(r"_\1", string).upper()

