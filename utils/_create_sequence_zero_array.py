
def _create_sequence_zero_array(space: Sequence):
    if space.stack:
        return create_zero_array(space.stacked_feature_space)
    else:
        return tuple()

