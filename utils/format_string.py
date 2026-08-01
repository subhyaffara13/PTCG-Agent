
def format_string(s: str, *, allow_multiline: bool) -> str:
    do_multiline = allow_multiline and "\n" in s
    if do_multiline:
        result = '"""\n'
        s = s.replace("\r\n", "\n")
    else:
        result = '"'

    pos = seq_start = 0
    while True:
        try:
            char = s[pos]
        except IndexError:
            result += s[seq_start:pos]
            if do_multiline:
                return result + '"""'
            return result + '"'
        if char in ILLEGAL_BASIC_STR_CHARS:
            result += s[seq_start:pos]
            if char in COMPACT_ESCAPES:
                if do_multiline and char == "\n":
                    result += "\n"
                else:
                    result += COMPACT_ESCAPES[char]
            else:
                result += "\\u" + hex(ord(char))[2:].rjust(4, "0")
            seq_start = pos + 1
        pos += 1


def format_string(s: str, *, allow_multiline: bool) -> str:
    do_multiline = allow_multiline and "\n" in s
    if do_multiline:
        result = '"""\n'
        s = s.replace("\r\n", "\n")
    else:
        result = '"'

    pos = seq_start = 0
    while True:
        try:
            char = s[pos]
        except IndexError:
            result += s[seq_start:pos]
            if do_multiline:
                return result + '"""'
            return result + '"'
        if char in ILLEGAL_BASIC_STR_CHARS:
            result += s[seq_start:pos]
            if char in COMPACT_ESCAPES:
                if do_multiline and char == "\n":
                    result += "\n"
                else:
                    result += COMPACT_ESCAPES[char]
            else:
                result += "\\u" + hex(ord(char))[2:].rjust(4, "0")
            seq_start = pos + 1
        pos += 1

