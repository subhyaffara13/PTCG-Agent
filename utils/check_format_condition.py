
def check_format_condition(condition: bool, error_message: str) -> None:
    if not condition:
        raise PdfFormatError(error_message)

