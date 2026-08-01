
def assemble_exception_table(tab: list[ExceptionTableEntry]) -> bytes:
    """
    Inverse of parse_exception_table - encodes list of exception
    table entries into bytes.
    """
    b = []
    for entry in tab:
        first_entry = encode_exception_table_varint(entry.start // 2)
        first_entry[0] |= 1 << 7
        b.extend(first_entry)
        length = entry.end - entry.start + 2
        b.extend(encode_exception_table_varint(length // 2))
        b.extend(encode_exception_table_varint(entry.target // 2))
        dl = (entry.depth << 1) + entry.lasti
        b.extend(encode_exception_table_varint(dl))
    return bytes(b)

