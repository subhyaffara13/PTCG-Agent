from typing import Callable

def _escape(s: str, escaping: str, valid_rune_fn: Callable[[str, int], bool]) -> str:
    """Performs backslash escaping on backslash, newline, and double-quote characters.

    valid_rune_fn takes the input character and its index in the containing string."""
    if escaping == ALLOWUTF8:
        return s.replace('\\', r'\\').replace('\n', r'\n').replace('"', r'\"')
    elif escaping == UNDERSCORES:
        escaped = StringIO()
        for i, b in enumerate(s):
            if valid_rune_fn(b, i):
                escaped.write(b)
            else:
                escaped.write('_')
        return escaped.getvalue()
    elif escaping == DOTS:
        escaped = StringIO()
        for i, b in enumerate(s):
            if b == '_':
                escaped.write('__')
            elif b == '.':
                escaped.write('_dot_')
            elif valid_rune_fn(b, i):
                escaped.write(b)
            else:
                escaped.write('__')
        return escaped.getvalue()
    elif escaping == VALUES:
        escaped = StringIO()
        escaped.write("U__")
        for i, b in enumerate(s):
            if b == '_':
                escaped.write("__")
            elif valid_rune_fn(b, i):
                escaped.write(b)
            elif not _is_valid_utf8(b):
                escaped.write("_FFFD_")
            else:
                escaped.write('_')
                escaped.write(format(ord(b), 'x'))
                escaped.write('_')
        return escaped.getvalue()
    return s


def _escape(x):
  """Returns a newline-free backslash-escaped version of the given string."""
  x = x.replace("\\", R"\\")
  x = x.replace("\n", R"\n")
  return x

