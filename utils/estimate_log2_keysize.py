
def estimate_log2_keysize(n: int) -> int:
    # 7 == HT_MINSIZE - 1
    return (((n * 3 + 1) // 2) | 7).bit_length()

