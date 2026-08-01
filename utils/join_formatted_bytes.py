
def join_formatted_bytes(
    builder: IRBuilder, literals: list[str], substitutions: list[Value], line: int
) -> Value:
    """Merge the list of literals and the list of substitutions
    alternatively using 'bytes_build_op'."""
    result_list: list[Value] = [Integer(0, c_pyssize_t_rprimitive)]

    for a, b in zip(literals, substitutions):
        if a:
            result_list.append(builder.load_bytes_from_str_literal(a))
        result_list.append(b)
    if literals[-1]:
        result_list.append(builder.load_bytes_from_str_literal(literals[-1]))

    # Special case for empty bytes and literal
    if len(result_list) == 1:
        return builder.load_bytes_from_str_literal("")
    if not substitutions and len(result_list) == 2:
        return result_list[1]

    result_list[0] = Integer(len(result_list) - 1, c_pyssize_t_rprimitive)
    return builder.call_c(bytes_build_op, result_list, line)

