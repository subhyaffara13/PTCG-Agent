
def outdent(code, spaces=None, all=True):
    '''outdent a block of code (default is to strip all leading whitespace)'''
    indent = indentsize(code)
    if spaces is None or spaces > indent or spaces < 0: spaces = indent
    #XXX: will this delete '\n' in some cases?
    if not all: return code[spaces:]
    return '\n'.join(_outdent(code.split('\n'), spaces=spaces, all=all))

