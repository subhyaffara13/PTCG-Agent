
def _make_unpacked_invalid_op(op_name: str):
    op = make_invalid_op(op_name)
    return unpack_zerodim_and_defer(op_name)(op)

