
def generate_format_ops(specifiers: list[ConversionSpecifier]) -> list[FormatOp] | None:
    """Convert ConversionSpecifier to FormatOp.

    Different ConversionSpecifiers may share a same FormatOp.
    """
    format_ops = []
    for spec in specifiers:
        # TODO: Match specifiers instead of using whole_seq
        if spec.whole_seq == "%s" or spec.whole_seq == "{:{}}":
            format_op = FormatOp.STR
        elif spec.whole_seq == "%d":
            format_op = FormatOp.INT
        elif spec.whole_seq == "%b":
            format_op = FormatOp.BYTES
        elif spec.whole_seq:
            return None
        else:
            format_op = FormatOp.STR
        format_ops.append(format_op)
    return format_ops

