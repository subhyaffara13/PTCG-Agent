
def _frozenconfigdict_valid_input(obj, ancestor_list=None):
  """Raises error if obj is NOT a valid input for FrozenConfigDict.

  Args:
    obj: Object to check. In the first call (with ancestor_list = None), obj
        should be of type ConfigDict. During recursion, it may be any type
        except dict.
    ancestor_list: List of ancestors of obj in the attribute/element
        structure, used to detect reference cycles in obj.

  Raises:
    ValueError: If obj is an invalid input for FrozenConfigDict, i.e. if it
        contains a dict within a list/tuple or contains a reference cycle. Also
        if obj is a dict, which means it wasn't already converted to ConfigDict.
  """
  ancestor_list = ancestor_list or []

  # Dicts must be converted to ConfigDict before _frozenconfigdict_valid_input()
  assert not isinstance(obj, dict)

  if id(obj) in ancestor_list:
    raise ValueError('Bad FrozenConfigDict initialization: Cannot contain a '
                     'cycle in its reference structure.')
  ancestor_list.append(id(obj))

  if isinstance(obj, ConfigDict):
    for value in obj.values():
      _frozenconfigdict_valid_input(value, ancestor_list)
  elif isinstance(obj, FieldReference):
    _frozenconfigdict_valid_input(obj.get(), ancestor_list)
  elif isinstance(obj, (list, tuple)):
    for element in obj:
      if isinstance(element, (dict, ConfigDict, FieldReference)):
        raise ValueError('Bad FrozenConfigDict initialization: Cannot '
                         'contain a dict, ConfigDict, or FieldReference '
                         'within a list or tuple.')
      _frozenconfigdict_valid_input(element, ancestor_list)
  ancestor_list.pop()

