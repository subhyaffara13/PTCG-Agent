
def format_error_message(host_error: str, exception: BaseException) -> str:
    if not exception.args:
        return f"Error connecting to {host_error}."
    elif len(exception.args) == 1:
        return f"Error {exception.args[0]} connecting to {host_error}."
    else:
        return (
            f"Error {exception.args[0]} connecting to {host_error}. "
            f"{exception.args[1]}."
        )

