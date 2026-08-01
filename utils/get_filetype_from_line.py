
def get_filetype_from_line(l): # noqa: E741
    m = modeline_re.search(l)
    if m:
        return m.group(1)


def get_filetype_from_line(l): # noqa: E741
    m = modeline_re.search(l)
    if m:
        return m.group(1)

