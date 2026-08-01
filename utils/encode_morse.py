
def encode_morse(msg, sep='|', mapping=None):
    """
    Encodes a plaintext into popular Morse Code with letters
    separated by ``sep`` and words by a double ``sep``.

    Examples
    ========

    >>> from sympy.crypto.crypto import encode_morse
    >>> msg = 'ATTACK RIGHT FLANK'
    >>> encode_morse(msg)
    '.-|-|-|.-|-.-.|-.-||.-.|..|--.|....|-||..-.|.-..|.-|-.|-.-'

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Morse_code

    """

    mapping = mapping or char_morse
    assert sep not in mapping
    word_sep = 2*sep
    mapping[" "] = word_sep
    suffix = msg and msg[-1] in whitespace

    # normalize whitespace
    msg = (' ' if word_sep else '').join(msg.split())
    # omit unmapped chars
    chars = set(''.join(msg.split()))
    ok = set(mapping.keys())
    msg = translate(msg, None, ''.join(chars - ok))

    morsestring = []
    words = msg.split()
    for word in words:
        morseword = []
        for letter in word:
            morseletter = mapping[letter]
            morseword.append(morseletter)

        word = sep.join(morseword)
        morsestring.append(word)

    return word_sep.join(morsestring) + (word_sep if suffix else '')

