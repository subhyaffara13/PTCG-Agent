
def emit_await(builder: IRBuilder, val: Value, line: int) -> Value:
    return emit_yield_from_or_await(builder, val, line, is_await=True)

