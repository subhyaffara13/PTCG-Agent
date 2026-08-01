
def split_comments(lines_enum: ReqFileLines) -> ReqFileLines:
    """
    Split comments from text, strip text and filter empty lines.
    Yield TextLine or Commentline
    """
    for line_number, line in lines_enum:
        parts = [l.strip() for l in COMMENT_RE.split(line) if l.strip()]

        if len(parts) == 1:
            part = parts[0]
            if part.startswith('#'):
                yield CommentLine(line_number=line_number, line=part)
            else:
                yield TextLine(line_number=line_number, line=part)

        elif len(parts) == 2:
            line, comment = parts
            yield TextLine(line_number=line_number, line=line)
            yield CommentLine(line_number=line_number, line=comment)

        else:
            if parts:
                # this should not ever happen
                raise Exception(f"Invalid line/comment: {line!r}")

