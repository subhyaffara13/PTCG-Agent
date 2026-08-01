
def try_specialize_str_index_compare(
    builder: IRBuilder, op: str, lhs: Expression, rhs: Expression, line: int
) -> Value | None:
    """Specialize `s[i] == 'x'` / `s[i] != 'x'` (and the symmetric form with
    operands swapped) into an int compare of codepoints.

    Returns None if the pattern doesn't match: the indexed base must be str,
    the index must be an integer, and the literal must be a 1-character str.
    Multi-character or empty literals fall through to the generic str compare
    (which still returns False for them, matching today's behavior).
    """
    # Normalize so the IndexExpr is on the left.
    if isinstance(rhs, IndexExpr) and not isinstance(lhs, IndexExpr):
        tmp = lhs
        lhs, rhs = rhs, tmp
    # Shape: s[i] {==, !=} "x" where "x" is exactly one codepoint.
    if (
        not isinstance(lhs, IndexExpr)
        or not isinstance(rhs, StrExpr)
        or len(rhs.value) != 1
        or not is_str_rprimitive(builder.node_type(lhs.base))
    ):
        return None
    index_type = builder.node_type(lhs.index)
    if not (is_tagged(index_type) or is_fixed_width_rtype(index_type)):
        return None

    # ord(s[i]) with bounds check; raises IndexError for out-of-range indices,
    # matching the behavior of the generic s[i] path.
    codepoint = translate_getitem_with_bounds_check(
        builder,
        lhs.base,
        [lhs.index],
        lhs,
        str_adjust_index_op,
        str_range_check_op,
        str_get_item_unsafe_as_int_op,
    )
    if codepoint is None:
        return None
    literal_cp = Integer(ord(rhs.value), short_int_rprimitive, line)
    return builder.binary_op(codepoint, literal_cp, op, line)

