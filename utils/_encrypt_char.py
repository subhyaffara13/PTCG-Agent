
def _encryptChar(plain, R):
    plain = byteord(plain)
    cipher = ((plain ^ (R >> 8))) & 0xFF
    R = ((cipher + R) * 52845 + 22719) & 0xFFFF
    return bytechr(cipher), R

