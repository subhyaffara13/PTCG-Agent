
def encipher_rot13(msg, symbols=None):
    """
    Performs the ROT13 encryption on a given plaintext ``msg``.

    Explanation
    ===========

    ROT13 is a substitution cipher which substitutes each letter
    in the plaintext message for the letter furthest away from it
    in the English alphabet.

    Equivalently, it is just a Caeser (shift) cipher with a shift
    key of 13 (midway point of the alphabet).

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/ROT13

    See Also
    ========

    decipher_rot13
    encipher_shift

    """
    return encipher_shift(msg, 13, symbols)

