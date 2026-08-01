
def _bit_list_to_bytes(bit_list):
    """Converts an iterable of 1s and 0s to bytes.

    Combines the list 8 at a time, treating each group of 8 bits
    as a single byte.

    Args:
        bit_list (Sequence): Sequence of 1s and 0s.

    Returns:
        bytes: The decoded bytes.
    """
    num_bits = len(bit_list)
    byte_vals = bytearray()
    for start in range(0, num_bits, 8):
        curr_bits = bit_list[start : start + 8]
        char_val = sum(val * digit for val, digit in zip(_POW2, curr_bits))
        byte_vals.append(char_val)
    return bytes(byte_vals)

