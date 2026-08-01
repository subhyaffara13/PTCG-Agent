
def fontInfoStyleMapStyleNameValidator(value: Any) -> bool:
    """
    Version 2+.
    """
    options = ["regular", "italic", "bold", "bold italic"]
    return value in options

