
def join_formatted_strings(
    builder: IRBuilder, literals: list[str] | None, substitutions: list[Value], line: int
) -> Value:
    """Merge the list of literals and the list of substitutions
    alternatively using 'str_build_op'.

    `substitutions` is the result value of formatting conversions.

    If the `literals` is set to None, we simply join the substitutions;
    Otherwise, the `literals` is the literal substrings of the original
    format string and its length should be exactly one more than
    substitutions.

    For example:
    (1)    'This is a %s and the value is %d'
        -> literals: ['This is a ', ' and the value is', '']
    (2)    '{} and the value is {}'
        -> literals: ['', ' and the value is', '']
    """
    # The first parameter for str_build_op is the total size of
    # the following PyObject*
    result_list: list[Value] = [Integer(0, c_pyssize_t_rprimitive)]

    if literals is not None:
        for a, b in zip(literals, substitutions):
            if a:
                result_list.append(builder.load_str(a))
            result_list.append(b)
        if literals[-1]:
            result_list.append(builder.load_str(literals[-1]))
    else:
        result_list.extend(substitutions)

    # Special case for empty string and literal string
    if len(result_list) == 1:
        return builder.load_str("")
    if not substitutions and len(result_list) == 2:
        return result_list[1]

    result_list[0] = Integer(len(result_list) - 1, c_pyssize_t_rprimitive)
    return builder.call_c(str_build_op, result_list, line)

