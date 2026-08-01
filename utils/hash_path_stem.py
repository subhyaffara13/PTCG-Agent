
def hash_path_stem(s: str) -> int:
    """Hash the stem of a cache file path (everything before the first dot in the basename).

    This is a combined stem-extraction + hash function optimized for mypyc compilation.
    Uses only integer arithmetic, avoiding intermediate string allocations.
    """
    # First find end of stem (scanning backwards, stop at first dot after last separator)
    i = len(s) - 1
    end: i64 = i
    while i >= 0:
        c: i64 = ord(s[i])
        if c == ord("/") or c == ord("\\"):
            break
        if c == ord("."):
            end = i
        i -= 1
    # Calculate hash
    hv: i64 = 123
    i = end
    while i >= 0:
        c = i64(ord(s[i]))
        hv = (hv * 33) ^ c
        i -= 1
    # Murmur3 finalizer for better bit avalanche (improves shard uniformity)
    hv = (hv ^ (hv >> 32)) & 0xFFFFFFFF
    hv ^= hv >> 16
    hv = (hv * 0x85EBCA6B) & 0xFFFFFFFF
    hv ^= hv >> 13
    hv = (hv * 0xC2B2AE35) & 0xFFFFFFFF
    hv ^= hv >> 16
    return int(hv)

