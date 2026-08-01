
def getIntEncoder(format):
    if format == "cff":
        twoByteOp = bytechr(28)
        fourByteOp = bytechr(29)
    elif format == "t1":
        twoByteOp = None
        fourByteOp = bytechr(255)
    else:
        assert format == "t2"
        twoByteOp = bytechr(28)
        fourByteOp = None

    def encodeInt(
        value,
        fourByteOp=fourByteOp,
        bytechr=bytechr,
        pack=struct.pack,
        unpack=struct.unpack,
        twoByteOp=twoByteOp,
    ):
        if -107 <= value <= 107:
            code = bytechr(value + 139)
        elif 108 <= value <= 1131:
            value = value - 108
            code = bytechr((value >> 8) + 247) + bytechr(value & 0xFF)
        elif -1131 <= value <= -108:
            value = -value - 108
            code = bytechr((value >> 8) + 251) + bytechr(value & 0xFF)
        elif twoByteOp is not None and -32768 <= value <= 32767:
            code = twoByteOp + pack(">h", value)
        elif fourByteOp is None:
            # Backwards compatible hack: due to a previous bug in FontTools,
            # 16.16 fixed numbers were written out as 4-byte ints. When
            # these numbers were small, they were wrongly written back as
            # small ints instead of 4-byte ints, breaking round-tripping.
            # This here workaround doesn't do it any better, since we can't
            # distinguish anymore between small ints that were supposed to
            # be small fixed numbers and small ints that were just small
            # ints. Hence the warning.
            log.warning(
                "4-byte T2 number got passed to the "
                "IntType handler. This should happen only when reading in "
                "old XML files.\n"
            )
            code = bytechr(255) + pack(">l", value)
        else:
            code = fourByteOp + pack(">l", value)
        return code

    return encodeInt

