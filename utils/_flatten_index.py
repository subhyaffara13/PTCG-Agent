
def _flatten_index(indices, width):
    result = indices[0]
    for d in range(1, len(indices)):
        result = width[d] * result + indices[d]
    return result

