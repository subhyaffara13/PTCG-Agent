
def diff_ranges(
    left: list[str], right: list[str]
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    seq = difflib.SequenceMatcher(None, left, right)
    # note last triple is a dummy, so don't need to worry
    blocks = seq.get_matching_blocks()

    i = 0
    j = 0
    left_ranges = []
    right_ranges = []
    for block in blocks:
        # mismatched range
        left_ranges.append((i, block.a))
        right_ranges.append((j, block.b))

        i = block.a + block.size
        j = block.b + block.size

        # matched range
        left_ranges.append((block.a, i))
        right_ranges.append((block.b, j))
    return left_ranges, right_ranges

