
def _aligned_offset(offset, alignment):
    # round up offset:
    return - (-offset // alignment) * alignment

