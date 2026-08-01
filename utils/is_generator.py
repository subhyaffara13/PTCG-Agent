
def is_generator(code: types.CodeType) -> bool:
    co_generator = 0x20
    return (code.co_flags & co_generator) > 0

