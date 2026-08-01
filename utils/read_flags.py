
def read_flags(data: ReadBuffer, num_flags: int) -> list[bool]:
    packed = read_int(data)
    return [(packed & (1 << i)) != 0 for i in range(num_flags)]

