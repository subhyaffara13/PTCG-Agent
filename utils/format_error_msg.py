
def format_error_msg(
    exc: Exception,
    code: types.CodeType,
    record_filename: str | None = None,
    frame: DynamoFrameType | None = None,
) -> str:
    if config.verbose:
        return format_error_msg_verbose(exc, code, record_filename, frame)
    return f"WON'T CONVERT {code.co_name} {code.co_filename}\
 line {code.co_firstlineno} \ndue to: \n{format_exc()}"

