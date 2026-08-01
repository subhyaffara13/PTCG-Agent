
def paragraph_is_fully_commented(lines, comment, main_language):
    """Is the paragraph fully commented?"""
    for i, line in enumerate(lines):
        if line.startswith(comment):
            if line[len(comment) :].lstrip().startswith(comment):
                continue
            if is_magic(line, main_language):
                return False
            continue
        return i > 0 and _BLANK_LINE.match(line)
    return True

