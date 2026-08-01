
def extract_type(name: str) -> str:
    """If the argument is the name of a method (of form C.m), return
    the type portion in quotes (e.g. "y"). Otherwise, return the string
    unmodified.
    """
    name = re.sub('^"[a-zA-Z0-9_]+" of ', "", name)
    return name

