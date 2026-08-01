
def _process_group_color(ranks: list[int]) -> int:
    # Convert list to tuple to make it hashable
    # pyrefly: ignore [bad-assignment]
    ranks = tuple(ranks)
    hash_value = hash(ranks)
    # Split color must be:
    # - a non-negative integer;
    # - a type compatible with C's int because we are pybinding to the latter.
    # Thus, we limit the hash value within c_int's max value.
    max_c_int = 2 ** (ctypes.sizeof(ctypes.c_int) * 8 - 1)
    color = abs(hash_value) % max_c_int
    return color

