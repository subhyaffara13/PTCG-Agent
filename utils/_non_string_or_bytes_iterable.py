
def _non_string_or_bytes_iterable(obj):
  return (isinstance(obj, abc.Iterable) and not isinstance(obj, str) and
          not isinstance(obj, bytes))

