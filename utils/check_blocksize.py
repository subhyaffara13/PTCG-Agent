
def check_blocksize(f_name, blocksize):
    if len(blocksize) != 2:
        raise AssertionError(f"blocksize must have length 2, got {len(blocksize)}")

    def is_power_of_two(v):
        return not (v & (v - 1))

    def is_compatible_blocksize(b):
        res = True
        for blocksize in b:
            # Triton loads only blocks which are at least 16 and powers of 2.
            res = (blocksize >= 16 and is_power_of_two(blocksize)) and res
        return res

    check(
        is_compatible_blocksize(blocksize),
        f"{f_name}(): sparse inputs' blocksize ({blocksize[0]}, {blocksize[1]}) "
        "should be at least 16 and a power of 2 in each dimension.",
    )

