
def trojansource(context):
    src_data = context.file_data
    src_data.seek(0)
    encoding, _ = detect_encoding(src_data.readline)
    src_data.seek(0)
    for lineno, line in enumerate(
        src_data.read().decode(encoding).splitlines(), start=1
    ):
        for char in BIDI_CHARACTERS:
            try:
                col_offset = line.index(char) + 1
            except ValueError:
                continue
            text = (
                "A Python source file contains bidirectional"
                " control characters (%r)." % char
            )
            b_issue = bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.MEDIUM,
                cwe=issue.Cwe.INAPPROPRIATE_ENCODING_FOR_OUTPUT_CONTEXT,
                text=text,
                lineno=lineno,
                col_offset=col_offset,
            )
            b_issue.linerange = [lineno]
            return b_issue

