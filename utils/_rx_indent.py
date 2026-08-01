
def _rx_indent(level):
    # Kconfig *always* interprets a tab as 8 spaces, so this is the default.
    # Edit this if you are in an environment where KconfigLexer gets expanded
    # input (tabs expanded to spaces) and the expansion tab width is != 8,
    # e.g. in connection with Trac (trac.ini, [mimeviewer], tab_width).
    # Value range here is 2 <= {tab_width} <= 8.
    tab_width = 8
    # Regex matching a given indentation {level}, assuming that indentation is
    # a multiple of {tab_width}. In other cases there might be problems.
    if tab_width == 2:
        space_repeat = '+'
    else:
        space_repeat = '{1,%d}' % (tab_width - 1)
    if level == 1:
        level_repeat = ''
    else:
        level_repeat = f'{{{level}}}'
    return rf'(?:\t| {space_repeat}\t| {{{tab_width}}}){level_repeat}.*\n'

