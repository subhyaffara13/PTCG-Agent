
def check_regex_or_str_match(request_body_value: Any, regex_str: str) -> bool:
    """
    Check if request_body_value matches the regex_str or is equal to param
    """
    if re.match(regex_str, request_body_value) or regex_str == request_body_value:
        return True
    return False

