
def _trailingZeros(val: int, maxBits: int) -> int:
    if val == 0:
        return maxBits
    count = 0
    while (val & 1) == 0:
        val >>= 1
        count += 1
    return count

