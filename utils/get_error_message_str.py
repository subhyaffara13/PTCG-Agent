
def get_error_message_str(e: Exception) -> str:
    error_message = ""
    if isinstance(e, HTTPException):
        if isinstance(e.detail, str):
            error_message = e.detail
        elif isinstance(e.detail, dict):
            error_message = json.dumps(e.detail)
        elif hasattr(e, "message"):
            _error = getattr(e, "message", None)
            if isinstance(_error, str):
                error_message = _error
            elif isinstance(_error, dict):
                error_message = json.dumps(_error)
        else:
            error_message = str(e)
    else:
        error_message = str(e)
    return error_message

