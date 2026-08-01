
def _make_distinct_arena_arrays(n, prefix_a="A", prefix_b="B"):
    """Make two arrays with distinct dtype instances and equal arena layouts.

    All strings are longer than 15 bytes, so every entry lives in its
    descriptor's arena. Lengths match between the two arrays but contents
    differ, so an entry resolved through the wrong descriptor's arena reads
    detectably wrong data.
    """
    a_list = [f"{prefix_a * 10}{i:06d}" for i in range(n)]
    b_list = [f"{prefix_b * 10}{i:06d}" for i in range(n)]
    a = np.array(a_list, dtype="T")
    b = np.array(b_list, dtype="T")
    assert a.dtype is not b.dtype
    return a, b, np.array(a_list, dtype=object), np.array(b_list, dtype=object)

