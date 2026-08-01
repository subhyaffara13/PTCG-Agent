
def is_valid_name(name: str):
    """
    Return True if the name is a valid Python package name
    per:
    - https://www.python.org/dev/peps/pep-0426/#name
    - https://www.python.org/dev/peps/pep-0508/#names
    """
    return name and IS_VALID_NAME(name)

