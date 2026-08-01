
def _divide_last(null):
    """Normalize the nullspace by the rightmost non-zero entry."""
    null = null.to_field()

    if null.is_zero_matrix:
        return null

    rows = []
    for i in range(null.shape[0]):
        for j in reversed(range(null.shape[1])):
            if null[i, j]:
                rows.append(null[i, :] / null[i, j])
                break
        else:
            assert False # pragma: no cover

    return DomainMatrix.vstack(*rows)

