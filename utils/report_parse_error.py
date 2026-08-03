import re

def report_parse_error(error: ParseError, errors: Errors) -> None:
    message = error["message"]
    # Standardize error message by capitalizing the first word
    message = re.sub(r"^(\s*\w)", lambda m: m.group(1).upper(), message)
    # Respect blocker status from error, default to True for syntax errors
    is_blocker = error.get("blocker", True)
    error_code = error.get("code")
    if error_code is None:
        error_code = codes.SYNTAX
    else:
        # Fallback to [syntax] for backwards compatibility.
        error_code = codes.error_codes.get(error_code) or codes.SYNTAX
    errors.report(error["line"], error["column"], message, blocker=is_blocker, code=error_code)

