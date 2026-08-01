
def to_camel(snake: str) -> str:
    """Convert a snake_case string to camelCase.

    Args:
        snake: The string to convert.

    Returns:
        The converted camelCase string.
    """
    # If the string is already in camelCase and does not contain a digit followed
    # by a lowercase letter, return it as it is
    if re.match('^[a-z]+[A-Za-z0-9]*$', snake) and not re.search(r'\d[a-z]', snake):
        return snake

    camel = to_pascal(snake)
    return re.sub('(^_*[A-Z])', lambda m: m.group(1).lower(), camel)


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))

