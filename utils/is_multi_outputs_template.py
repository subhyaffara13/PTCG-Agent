
def is_multi_outputs_template(input_buf: Buffer | Operation | None) -> bool:
    """
    Check if input buffer is a multi-outputs template buffer
    """
    from . import ir

    return (
        isinstance(input_buf, ir.TemplateBuffer)
        and input_buf.is_multi_outputs_template()
    )

