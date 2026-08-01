
def _encodeHeader(branchFactor: int, height: int) -> bytes:
    branchFactorToId = {2: 0, 4: 1, 8: 2, 32: 3}
    return bytes([(height << 2) | branchFactorToId[branchFactor]])

