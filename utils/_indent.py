
def _indent(s, indent=4):
    """
    Add the given number of space characters to the beginning of
    every non-blank line in ``s``, and return the result.
    If the string ``s`` is Unicode, it is encoded using the stdout
    encoding and the ``backslashreplace`` error handler.
    """
    # This regexp matches the start of non-blank lines:
    return re.sub('(?m)^(?!$)', indent*' ', s)


def _indent(x, num_spaces):
  indent_str = ' ' * num_spaces
  lines = x.split('\n')
  assert not lines[-1]
  # skip the final line because it's empty and should not be indented.
  return '\n'.join(indent_str + line for line in lines[:-1]) + '\n'


def _indent(x: str, num_spaces: int):
  indent_str = ' ' * num_spaces
  lines = x.split('\n')
  # skip last line because it is always empty and should not be indented.
  assert not lines[-1]
  return '\n'.join(indent_str + line for line in lines[:-1]) + '\n'


def _indent(text, prefix, predicate=default_predicate) -> str:
    """Adds 'prefix' to the beginning of selected lines in 'text'.

    If 'predicate' is provided, 'prefix' will only be added to the lines
    where 'predicate(line)' is True. If 'predicate' is not provided,
    it will default to adding 'prefix' to all non-empty lines that do not
    consist solely of whitespace characters.
    """

    def prefixed_lines():
        for line in text.splitlines(True):
            yield prefix + line if predicate(line) else line

    return "".join(prefixed_lines())

