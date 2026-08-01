
def flagEncodeCoord(flag, mask, coord, coordBytes):
    byteCount = _flagSignBytes[flag & mask]
    if byteCount == 1:
        coordBytes.append(coord)
    elif byteCount == -1:
        coordBytes.append(-coord)
    elif byteCount == 2:
        coordBytes.extend(struct.pack(">h", coord))

