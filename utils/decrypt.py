
def decrypt(cipherstring, R):
    r"""
    Decrypts a string using the Type 1 encryption algorithm.

    Args:
            cipherstring: String of ciphertext.
            R: Initial key.

    Returns:
            decryptedStr: Plaintext string.
            R: Output key for subsequent decryptions.

    Examples::

            >>> testStr = b"\0\0asdadads asds\265"
            >>> decryptedStr, R = decrypt(testStr, 12321)
            >>> decryptedStr == b'0d\nh\x15\xe8\xc4\xb2\x15\x1d\x108\x1a<6\xa1'
            True
            >>> R == 36142
            True
    """
    plainList = []
    for cipher in cipherstring:
        plain, R = _decryptChar(cipher, R)
        plainList.append(plain)
    plainstring = bytesjoin(plainList)
    return plainstring, int(R)

