
def remapComponentsFast(self, glyphidmap):
    if not self.data or struct.unpack(">h", self.data[:2])[0] >= 0:
        return  # Not composite
    data = self.data = bytearray(self.data)
    i = 10
    more = 1
    while more:
        flags = (data[i] << 8) | data[i + 1]
        glyphID = (data[i + 2] << 8) | data[i + 3]
        # Remap
        glyphID = glyphidmap[glyphID]
        data[i + 2] = glyphID >> 8
        data[i + 3] = glyphID & 0xFF
        i += 4
        flags = int(flags)

        if flags & 0x0001:
            i += 4  # ARG_1_AND_2_ARE_WORDS
        else:
            i += 2
        if flags & 0x0008:
            i += 2  # WE_HAVE_A_SCALE
        elif flags & 0x0040:
            i += 4  # WE_HAVE_AN_X_AND_Y_SCALE
        elif flags & 0x0080:
            i += 8  # WE_HAVE_A_TWO_BY_TWO
        more = flags & 0x0020  # MORE_COMPONENTS

