
def _decodeHeader(headerByte: int) -> Tuple[int, int]:
    id = headerByte & 0x03
    idToBranchFactor = {0: 2, 1: 4, 2: 8, 3: 32}
    height = (headerByte >> 2) & 0x1F
    return idToBranchFactor[id], height

