
def parse_repl_hex_escape(source, expected_len, type):
    "Parses a hex escape sequence in a replacement string."
    digits = []
    for i in range(expected_len):
        ch = source.get()
        if ch not in HEX_DIGITS:
            raise error("incomplete escape \\%s%s" % (type, ''.join(digits)),
              source.string, source.pos)
        digits.append(ch)

    return int("".join(digits), 16)

