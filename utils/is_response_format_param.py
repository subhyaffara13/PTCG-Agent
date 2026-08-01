
def is_response_format_param(response_format: object) -> TypeGuard[ResponseFormatParam]:
    return is_dict(response_format)

