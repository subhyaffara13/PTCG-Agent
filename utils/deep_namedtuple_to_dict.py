
def deep_namedtuple_to_dict(obj):
  """Recursively converts namedtuples and tuples within a PyTree to dicts and lists.

  Args:
    obj: The object (PyTree) to convert.

  Returns:
    A new object with namedtuples converted to dicts and tuples converted to
    lists, recursively. Other types are preserved.
  """
  if hasattr(obj, '_asdict'):  # Check if it's a namedtuple
    # Convert namedtuple to dict and recurse on its values
    return {k: deep_namedtuple_to_dict(v) for k, v in obj._asdict().items()}
  elif isinstance(obj, dict):
    # Recurse on dictionary values
    return {k: deep_namedtuple_to_dict(v) for k, v in obj.items()}
  elif isinstance(obj, list):
    # Recurse on list items
    return [deep_namedtuple_to_dict(elem) for elem in obj]
  elif isinstance(obj, tuple):
    # Convert tuple to list and recurse on its items
    return [deep_namedtuple_to_dict(elem) for elem in obj]
  else:
    # Base case: not a namedtuple, dict, list, or tuple
    return obj

