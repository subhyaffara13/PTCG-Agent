
def _process_string_or_callable(string_or_callable, dictionary):
  """Process a callable or a string representing a callable.

  Args:
    string_or_callable: Either a string or a callable
    dictionary: Dictionary of shape {string_reference: callable}

  Returns:
    string_or_callable if string_or_callable is a callable ; otherwise,
    dictionary[string_or_callable]

  Raises:
    NotImplementedError: If string_or_callable is of the wrong type, or has an
      unexpected value (Not present in dictionary).
  """
  if callable(string_or_callable):
    return string_or_callable

  try:
    return dictionary[string_or_callable]
  except KeyError as e:
    raise NotImplementedError("Input type / value not supported. Accepted types"
                              ": string, callable. Acceptable string values : "
                              "{}. Input provided : {}".format(
                                  list(dictionary.keys()),
                                  string_or_callable)) from e

