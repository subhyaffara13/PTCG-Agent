
def normalize_seq_array_like(x, parm=None):  # codespell:ignore
    return tuple(normalize_array_like(value) for value in x)

