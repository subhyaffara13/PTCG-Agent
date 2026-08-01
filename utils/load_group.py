
def load_group(value, group):
    """
    Given a value of an entry point or series of entry points,
    return each as an EntryPoint.
    """
    # normalize to a single sequence of lines
    lines = yield_lines(value)
    text = f'[{group}]\n' + '\n'.join(lines)
    return metadata.EntryPoints._from_text(text)

