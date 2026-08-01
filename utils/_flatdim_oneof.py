
def _flatdim_oneof(space: OneOf) -> int:
    return 1 + max(flatdim(s) for s in space.spaces)

