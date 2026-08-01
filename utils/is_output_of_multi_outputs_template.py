
def is_output_of_multi_outputs_template(
    input_buf: Buffer | Operation | None,
) -> bool:
    """
    Check if input buffer is a output of multi-outputs template buffer
    """
    from . import ir

    return (
        isinstance(input_buf, ir.MultiOutput)
        and len(input_buf.inputs) == 1
        and is_multi_outputs_template(input_buf.inputs[0])  # type: ignore[arg-type]
    )

