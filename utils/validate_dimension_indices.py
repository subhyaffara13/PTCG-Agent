
def validate_dimension_indices(rank: int, indices: DimsSequenceType):
    for idx in indices:
        validate_idx(rank, idx)

