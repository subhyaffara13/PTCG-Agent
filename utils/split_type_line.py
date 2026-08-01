
def split_type_line(type_line):
    """Split the comment with the type annotation into parts for argument and return types.

    For example, for an input of:
        # type: (Tensor, torch.Tensor) -> Tuple[Tensor, Tensor]

    This function will return:
        ("(Tensor, torch.Tensor)", "Tuple[Tensor, Tensor]")

    """
    start_offset = len("# type:")
    try:
        arrow_pos = type_line.index("->")
    except ValueError:
        raise RuntimeError(
            "Syntax error in type annotation (couldn't find `->`)"
        ) from None
    return type_line[start_offset:arrow_pos].strip(), type_line[arrow_pos + 2 :].strip()

