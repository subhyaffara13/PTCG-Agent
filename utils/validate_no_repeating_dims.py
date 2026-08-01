
def validate_no_repeating_dims(dims: Sequence):
    if len(dims) != len(set(dims)):
        raise RuntimeError("duplicate value in the list of dims")

