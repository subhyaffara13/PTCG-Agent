
def VarData_calculateNumShorts(self, optimize=False):
    count = self.VarRegionCount
    items = self.Item
    bit_lengths = [0] * count
    for item in items:
        # The "+ (i < -1)" magic is to handle two's-compliment.
        # That is, we want to get back 7 for -128, whereas
        # bit_length() returns 8. Similarly for -65536.
        # The reason "i < -1" is used instead of "i < 0" is that
        # the latter would make it return 0 for "-1" instead of 1.
        bl = [(i + (i < -1)).bit_length() for i in item]
        bit_lengths = [max(*pair) for pair in zip(bl, bit_lengths)]
    # The addition of 8, instead of seven, is to account for the sign bit.
    # This "((b + 8) >> 3) if b else 0" when combined with the above
    # "(i + (i < -1)).bit_length()" is a faster way to compute byte-lengths
    # conforming to:
    #
    # byte_length = (0 if i == 0 else
    # 		 1 if -128 <= i < 128 else
    # 		 2 if -65536 <= i < 65536 else
    # 		 ...)
    byte_lengths = [((b + 8) >> 3) if b else 0 for b in bit_lengths]

    # https://github.com/fonttools/fonttools/issues/2279
    longWords = any(b > 2 for b in byte_lengths)

    if optimize:
        # Reorder columns such that wider columns come before narrower columns
        mapping = []
        mapping.extend(i for i, b in enumerate(byte_lengths) if b > 2)
        mapping.extend(i for i, b in enumerate(byte_lengths) if b == 2)
        mapping.extend(i for i, b in enumerate(byte_lengths) if b == 1)

        byte_lengths = _reorderItem(byte_lengths, mapping)
        self.VarRegionIndex = _reorderItem(self.VarRegionIndex, mapping)
        self.VarRegionCount = len(self.VarRegionIndex)
        for i in range(len(items)):
            items[i] = _reorderItem(items[i], mapping)

    if longWords:
        self.NumShorts = (
            max((i for i, b in enumerate(byte_lengths) if b > 2), default=-1) + 1
        )
        self.NumShorts |= 0x8000
    else:
        self.NumShorts = (
            max((i for i, b in enumerate(byte_lengths) if b > 1), default=-1) + 1
        )

    self.VarRegionCount = len(self.VarRegionIndex)
    return self

