
def line_width(line):
    """Unicode combining symbols (modifiers) are not ever displayed as
    separate symbols and thus should not be counted
    """
    return len(line.translate(_remove_combining))

