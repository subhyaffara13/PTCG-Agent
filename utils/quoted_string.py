
def quoted_string(content: str) -> str:
    """Return 7-bit content as quoted-string.

    Format content into a quoted-string as defined in RFC5322 for
    Internet Message Format. Notice that this is not the 8-bit HTTP
    format, but the 7-bit email format. Content must be in usascii or
    a ValueError is raised.
    """
    if not (QCONTENT > set(content)):
        raise ValueError(f"bad content for quoted-string {content!r}")
    return not_qtext_re.sub(lambda x: "\\" + x.group(0), content)

