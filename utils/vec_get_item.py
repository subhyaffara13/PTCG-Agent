
def vec_get_item(
    builder: LowLevelIRBuilder, base: Value, index: Value, line: int, *, can_borrow: bool = False
) -> Value:
    """Generate inlined vec __getitem__ call.

    We inline the length and bounds check, since they are simple but
    performance-critical. The actual item load is emitted as a generic primitive
    op that is lowered later.
    """
    # TODO: Support more index types
    len_val = vec_len(builder, base)
    index = vec_check_and_adjust_index(builder, len_val, index, line)
    return vec_get_item_unsafe(builder, base, index, line, can_borrow=can_borrow)

