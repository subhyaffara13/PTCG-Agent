
def encode_c_string_literal(b: bytes) -> str:
    """Convert bytestring to the C string literal syntax (with necessary escaping).

    For example, b'foo\n' gets converted to 'foo\\n' (note that double quotes are not added).
    """
    if not _translation_table:
        # Initialize the translation table on the first call.
        d = {
            ord("\n"): "\\n",
            ord("\r"): "\\r",
            ord("\t"): "\\t",
            ord('"'): '\\"',
            ord("\\"): "\\\\",
        }
        for i in range(256):
            if i not in d:
                if i < 32 or i >= 127:
                    d[i] = "\\x%.2x" % i
                else:
                    d[i] = chr(i)
        _translation_table.update(str.maketrans(d))
    return b.decode("latin1").translate(_translation_table)

