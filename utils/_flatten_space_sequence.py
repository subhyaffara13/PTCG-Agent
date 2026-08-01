
def _flatten_space_sequence(space: Sequence) -> Sequence:
    return Sequence(flatten_space(space.feature_space), stack=space.stack)


def _flatten_space_sequence(space: Sequence) -> Sequence:
    return Sequence(flatten_space(space.feature_space))

