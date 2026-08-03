import re

def split_by_unquoted(line, characters):
    """
    Splits the line into (line[:i], line[i:]),
    where i is the index of first occurrence of one of the characters
    not within quotes, or len(line) if no such index exists
    """
    assert not (set('"\'') & set(characters)), "cannot split by unquoted quotes"
    r = re.compile(
        r"\A(?P<before>({single_quoted}|{double_quoted}|{not_quoted})*)"
        r"(?P<after>{char}.*)\Z".format(
            not_quoted=f"[^\"'{re.escape(characters)}]",
            char=f"[{re.escape(characters)}]",
            single_quoted=r"('([^'\\]|(\\.))*')",
            double_quoted=r'("([^"\\]|(\\.))*")'))
    m = r.match(line)
    if m:
        d = m.groupdict()
        return (d["before"], d["after"])
    return (line, "")

