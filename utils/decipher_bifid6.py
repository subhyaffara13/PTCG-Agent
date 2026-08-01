
def decipher_bifid6(msg, key):
    r"""
    Performs the Bifid cipher decryption on ciphertext ``msg``, and
    returns the plaintext.

    This is the version of the Bifid cipher that uses the `6 \times 6`
    Polybius square.

    Parameters
    ==========

    msg
        Ciphertext string (digits okay); converted to upper case

    key
        Short string for key (digits okay).

        If ``key`` is less than 36 characters long, the square will be
        filled with letters A through Z and digits 0 through 9.
        All letters are converted to uppercase.

    Returns
    =======

    plaintext
        Plaintext from Bifid cipher (all caps, no spaces).

    Examples
    ========

    >>> from sympy.crypto.crypto import encipher_bifid6, decipher_bifid6
    >>> key = "gold bug"
    >>> encipher_bifid6('meet me on monday at 8am', key)
    'KFKLJJHF5MMMKTFRGPL'
    >>> decipher_bifid6(_, key)
    'MEETMEONMONDAYAT8AM'

    """
    msg, key, _ = _prep(msg.upper(), key.upper(), None, bifid6)
    key = padded_key(key, bifid6)
    return decipher_bifid(msg, '', key)

