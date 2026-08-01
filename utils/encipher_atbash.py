
def encipher_atbash(msg, symbols=None):
    r"""
    Enciphers a given ``msg`` into its Atbash ciphertext and returns it.

    Explanation
    ===========

    Atbash is a substitution cipher originally used to encrypt the Hebrew
    alphabet. Atbash works on the principle of mapping each alphabet to its
    reverse / counterpart (i.e. a would map to z, b to y etc.)

    Atbash is functionally equivalent to the affine cipher with ``a = 25``
    and ``b = 25``

    See Also
    ========

    decipher_atbash

    """
    return encipher_affine(msg, (25, 25), symbols)

