
def _bvalfromboundary(boundary):
    try:
        return _boundarydict[boundary] << 2
    except KeyError as e:
        raise ValueError("Acceptable boundary flags are 'fill', 'circular' "
                         "(or 'wrap'), and 'symmetric' (or 'symm').") from e

