
def _decryptChar(cipher, R):
    cipher = byteord(cipher)
    plain = ((cipher ^ (R >> 8))) & 0xFF
    R = ((cipher + R) * 52845 + 22719) & 0xFFFF
    return bytechr(plain), R

