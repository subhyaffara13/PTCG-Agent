
def indent(code, spaces=4):
    '''indent a block of code with whitespace (default is 4 spaces)'''
    indent = indentsize(code)
    from numbers import Integral
    if isinstance(spaces, Integral): spaces = ' '*spaces
    # if '\t' is provided, will indent with a tab
    nspaces = indentsize(spaces)
    # blank lines (etc) need to be ignored
    lines = code.split('\n')
##  stq = "'''"; dtq = '"""'
##  in_stq = in_dtq = False
    for i in range(len(lines)):
        #FIXME: works... but shouldn't indent 2nd+ lines of multiline doc
        _indent = indentsize(lines[i])
        if indent > _indent: continue
        lines[i] = spaces+lines[i]
##      #FIXME: may fail when stq and dtq in same line (depends on ordering)
##      nstq, ndtq = lines[i].count(stq), lines[i].count(dtq)
##      if not in_dtq and not in_stq:
##          lines[i] = spaces+lines[i] # we indent
##          # entering a comment block
##          if nstq%2: in_stq = not in_stq
##          if ndtq%2: in_dtq = not in_dtq
##      # leaving a comment block
##      elif in_dtq and ndtq%2: in_dtq = not in_dtq
##      elif in_stq and nstq%2: in_stq = not in_stq
##      else: pass
    if lines[-1].strip() == '': lines[-1] = ''
    return '\n'.join(lines)


def indent(func):
    """
    Decorator for allowing to use method as normal method or with
    context manager for auto-indenting code blocks.
    """
    def wrapper(self, line, *args, optimize=True, **kwds):
        last_line = self._indent_last_line
        line = func(self, line, *args, **kwds)
        # When two blocks have the same condition (such as value has to be dict),
        # do the check only once and keep it under one block.
        if optimize and last_line == line:
            self._code.pop()
        self._indent_last_line = line
        return Indent(self, line)
    return wrapper


def indent(s: str, n: int) -> str:
    """Indent all the lines in s (separated by newlines) by n spaces."""
    s = " " * n + s
    s = s.replace("\n", "\n" + " " * n)
    return s


def indent(val: str) -> str:
    return _indent(val, "    ")


def indent(s):
    return "\n".join(["\t" + line for line in s.splitlines()])


def indent(string, prefix=' ' * 4):
    """
    >>> indent('foo')
    '    foo'
    """
    return prefix + string


def indent(str, indent=4):
    indent_str = ' '*indent
    if str is None:
        return indent_str
    lines = str.split('\n')
    return '\n'.join(indent_str + l for l in lines)


def indent(text: str | None, indents: int = 1) -> str:
    if not text or not isinstance(text, str):
        return ""
    jointext = "".join(["\n"] + ["    "] * indents)
    return jointext.join(text.split("\n"))

