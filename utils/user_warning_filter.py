
def user_warning_filter(
    message, category, filename, lineno, file=None, line=None
) -> bool:
    return category is not UserWarning

