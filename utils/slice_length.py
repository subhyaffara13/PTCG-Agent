
def slice_length(s: slice, seq_len: int) -> int:
    start, stop, step = s.indices(seq_len)
    return max(0, (stop - start + (step - (1 if step > 0 else -1))) // step)

