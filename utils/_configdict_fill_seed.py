
def _configdict_fill_seed(seed, initial_dictionary, visit_map=None):
  """Fills an empty ConfigDict without copying previously visited nodes.

  Turns seed (an empty ConfigDict) into a ConfigDict version of
  initial_dictionary. Avoids infinite looping on a self-referencing
  initial_dictionary because if a value of initial_dictionary has been
  previously visited, that value is not re-converted to a ConfigDict. If a
  FieldReference is encountered which contains a dict or FrozenConfigDict, its
  contents will be converted to ConfigDict.

  Note: As described in the __init__() documentation, this will not
  replicate the structure of initial_dictionary if it contains
  self-references within lists, tuples, or other types. There is no warning
  or error in this case.

  Args:
    seed: Empty ConfigDict, to be filled in.
    initial_dictionary: The template on which seed is built. May be of type
        dict, ConfigDict or FrozenConfigDict.
    visit_map: Dictionary from memory addresses to values, storing the
        ConfigDict versions of dictionary values. visit_map need not contain
        (id(initial_dictionary), seed) as a key/value pair.

  Raises:
    TypeError: If seed is not a ConfigDict.
    ValueError: If seed is not an empty ConfigDict.
  """
  # These should be impossible to raise, since the public call-site in
  # __init__() pass in valid input, as does this method recursively.
  assert isinstance(seed, ConfigDict)
  assert not seed

  visit_map = visit_map or {}
  visit_map[id(initial_dictionary)] = seed

  if isinstance(initial_dictionary, ConfigDict):
    iteritems = initial_dictionary.iteritems(preserve_field_references=True)
  else:
    iteritems = initial_dictionary.items()

  for key, value in iteritems:
    if id(value) in visit_map:
      value = visit_map[id(value)]

    elif (isinstance(value, FieldReference) and value.get_type() is dict
          and seed.convert_dict):
      # If the reference is empty, we don't have to do dict -> ConfigDict
      # conversion.
      # Calling get() on an empty required reference would raise an error so we
      # need a special case for this.
      if value.empty():
        pass
      elif id(value.get()) in visit_map:
        value.set(visit_map[id(value.get())], False)
      else:
        value_cd = ConfigDict(
            type_safe=seed.is_type_safe,
            allow_dotted_keys=seed.allow_dotted_keys,
        )
        _configdict_fill_seed(value_cd, value.get(), visit_map)
        value.set(value_cd, False)

    elif isinstance(value, dict) and seed.convert_dict:
      value_cd = ConfigDict(
          type_safe=seed.is_type_safe,
          allow_dotted_keys=seed.allow_dotted_keys,
      )
      _configdict_fill_seed(value_cd, value, visit_map)
      value = value_cd

    elif isinstance(value, FrozenConfigDict):
      value = ConfigDict(value, allow_dotted_keys=seed.allow_dotted_keys)

    seed.__setattr__(key, value)

