
def format_error(err: ParseError) -> str:
    return f"{err['line']}:{err['column']}: error: {err['message']}"

