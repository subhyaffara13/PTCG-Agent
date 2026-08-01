
def is_json_metadata(text):
    """Is this a JSON metadata?"""
    first_curly_bracket = text.find("{")
    if first_curly_bracket < 0:
        return False

    first_equal_sign = text.find("=")
    if first_equal_sign < 0:
        return True

    return first_curly_bracket < first_equal_sign

