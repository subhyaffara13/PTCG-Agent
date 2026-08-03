import re

def unescape(s: str) -> str:
    return re.sub(r"\\([{}()+-.*?^$\[\]\s\\|])", r"\1", s)


def unescape(text):
    """Replace XML character references with the referenced characters"""

    def fixup(m):
        text = m.group(0)
        if text[1] == "#":
            # Character reference
            if text[2] == "x":
                code = int(text[3:-1], 16)
            else:
                code = int(text[2:-1])
        else:
            # Named entity
            try:
                code = htmlentitydefs.name2codepoint[text[1:-1]]
            except KeyError:
                return text  # leave unchanged
        try:
            return chr(code)
        except (ValueError, OverflowError):
            return text  # leave unchanged

    return re.sub("&(?:[0-9A-Za-z]+|#(?:[0-9]+|x[0-9A-Fa-f]+));", fixup, text)

