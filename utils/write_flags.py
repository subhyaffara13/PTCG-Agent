
def write_flags(data: WriteBuffer, flags: list[bool]) -> None:
    assert len(flags) <= 26, "This many flags not supported yet"
    packed = 0
    for i, flag in enumerate(flags):
        if flag:
            packed |= 1 << i
    write_int(data, packed)

