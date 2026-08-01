
def get_status_code(exception):
    if hasattr(exception, "status_code"):
        return exception.status_code
    # Default status codes for exceptions without a status_code attribute
    if exception.__name__ == "Timeout":
        return 408  # Request Timeout
    if exception.__name__ == "APIConnectionError":
        return 503  # Service Unavailable
    return 500  # Internal Server Error as default

