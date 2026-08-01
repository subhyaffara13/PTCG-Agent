
def _convert_str_to_tuple(string):
  """Function to convert a Python `str` object to a `tuple`.

  Args:
    string: The `str` to be converted.

  Returns:
    A `tuple` version of the string.

  Raises:
    ValueError: If the string is not a well formed `tuple`.
  """
  # literal_eval converts strings to int, tuple, list, float and dict,
  # booleans and None. It can also handle nested tuples.
  # It does not, however, handle elements of type set.
  try:
    value = ast.literal_eval(string)
  except ValueError:
    # A ValueError is raised by literal_eval if the string is not well
    # formed. This is probably because string represents a single string
    # element, e.g. string='abc', and a tuple of strings field was overridden by
    # repeated use of a flag (ie `--flag a --flag b` instead of
    # `--flag '("a", "b")'`).
    value = string
  except SyntaxError as exc:
    # The only other error that may be raised is a `SyntaxError` because
    # `literal_eval` calls the Python in-built `compile`. This error is
    # caused by parsing issues.
    if ',' not in string and ' ' not in string:
      # Most likely passed a single string that contained an operator -- e.g.
      # '/path/to/file' or 'file_pattern*'. If a comma isn't in the string, then
      # it can't have been a tuple, so assume it's an unquoted string.
      # If passed strings containing a comma (user probably expects conversion
      # to a tuple) or whitespace (user might expect implicit conversion to
      # tuple?) raise an exception.
      value = string
    else:
      msg = (
          f'Error while parsing string: {string} as tuple. If you intended to'
          ' pass the argument as a single element, use quotes such as `--flag'
          f' {repr(repr(string))}, otherwise insert quotes around each element.'
      )
      if ' ' in string:
        msg += (
            ' Use commas instead of whitespace as the separator between'
            ' elements.'
        )
      raise ValueError(msg) from exc

  # Make sure we return a tuple.
  if isinstance(value, tuple):
    return value
  elif (isinstance(value, collections.abc.Iterable) and
        not isinstance(value, str)):
    return tuple(value)
  else:
    return (value,)

