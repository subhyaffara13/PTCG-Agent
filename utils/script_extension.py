
def script_extension(char):
    """Return the script extension property assigned to the Unicode character
    'char' as a set of string.

    >>> script_extension("a") == {'Latn'}
    True
    >>> script_extension(chr(0x060C)) == {'Nkoo', 'Arab', 'Rohg', 'Thaa', 'Syrc', 'Gara', 'Yezi'}
    True
    >>> script_extension(chr(0x10FFFF)) == {'Zzzz'}
    True
    """
    code = byteord(char)
    i = bisect_right(ScriptExtensions.RANGES, code)
    value = ScriptExtensions.VALUES[i - 1]
    if value is None:
        # code points not explicitly listed for Script Extensions
        # have as their value the corresponding Script property value
        return {script(char)}
    return value

