
def down_size(size):
    if size[-1] % 2 != 0:
        raise AssertionError(f"{size} last dim not divisible by two")
    return (*size[:-1], size[-1] // 2)

