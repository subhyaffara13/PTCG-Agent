
def meta_repeat_interleave_Tensor(repeats, output_size=None):
    if output_size is None:
        raise RuntimeError("cannot repeat_interleave a meta tensor without output_size")
    return repeats.new_empty(output_size)

