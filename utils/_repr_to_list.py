
def _repr_to_list(value: torch.Tensor):
    """
    Converts a tensor into a sanitized multi-line string representation.

    Args:
        value (`torch.Tensor`): The tensor to represent.

    Returns:
        `list[str]`: List of string lines representing the tensor.
    """
    torch.set_printoptions(sci_mode=True, linewidth=120)
    with StringIO() as buf, redirect_stdout(buf):
        print(value)  # to redirected stdout to avoid line splits
        raw = buf.getvalue()
    return _sanitize_repr_for_diff(raw).splitlines()

