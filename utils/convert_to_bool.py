
def convert_to_bool(x: str) -> bool:
    """
    Converts a string to a bool.
    """
    if x.lower() in ["1", "y", "yes", "true"]:
        return True
    if x.lower() in ["0", "n", "no", "false"]:
        return False
    raise ValueError(f"{x} is not a value that can be converted to a bool.")

