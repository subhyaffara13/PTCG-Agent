
def format_error_msg_verbose(
    exc: Exception,
    code: types.CodeType,
    record_filename: str | None = None,
    frame: DynamoFrameType | None = None,
) -> str:
    msg = (
        f"WON'T CONVERT {code.co_name} {code.co_filename} line {code.co_firstlineno}\n"
    )
    msg += "=" * 10 + " TorchDynamo Stack Trace " + "=" * 10 + "\n"
    msg += format_exc()
    real_stack = get_real_stack(exc, frame)
    if real_stack is not None:
        msg += (
            "\n"
            + "=" * 10
            + " The above exception occurred while processing the following code "
            + "=" * 10
            + "\n\n"
        )
        msg += "".join(format_list(real_stack))
        msg += "\n"
        msg += "=" * 10

    return msg

