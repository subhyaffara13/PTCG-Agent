
def decode_morse(msg, sep='|', mapping=None):
    """
    Decodes a Morse Code with letters separated by ``sep``
    (default is '|') and words by `word_sep` (default is '||)
    into plaintext.

    Examples
    ========

    >>> from sympy.crypto.crypto import decode_morse
    >>> mc = '--|---|...-|.||.|.-|...|-'
    >>> decode_morse(mc)
    'MOVE EAST'

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Morse_code

    """

    mapping = mapping or morse_char
    word_sep = 2*sep
    characterstring = []
    words = msg.strip(word_sep).split(word_sep)
    for word in words:
        letters = word.split(sep)
        chars = [mapping[c] for c in letters]
        word = ''.join(chars)
        characterstring.append(word)
    rv = " ".join(characterstring)
    return rv

