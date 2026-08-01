
def has_rich_response_format(
    response_format: type[ResponseFormatT] | ResponseFormatParam | Omit,
) -> TypeGuard[type[ResponseFormatT]]:
    if not is_given(response_format):
        return False

    if is_response_format_param(response_format):
        return False

    return True

