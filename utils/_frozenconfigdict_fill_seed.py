
def _frozenconfigdict_fill_seed(seed, initial_configdict, visit_map=None):
  """Fills an empty FrozenConfigDict without copying previously visited nodes.

  Turns seed (an empty FrozenConfigDict) into a FrozenConfigDict version of
  initial_configdict. Avoids duplicating nodes of initial_configdict because if
  a value of initial_configdict has been previously visited, that value is not
  re-converted to a FrozenConfigDict. If a FieldReference is encountered which
  contains a dict, its contents will be converted to FrozenConfigDict.

  Note: As described in the __init__() documentation, this will not
  replicate the structure of initial_configdict if it contains
  self-references within lists, tuples, or other types. There is no warning
  or error in this case.

  Args:
    seed: Empty FrozenConfigDict, to be filled in.
    initial_configdict: The template on which seed is built. Must be of type
        ConfigDict.
    visit_map: Dictionary from memory addresses to values, storing the
        FrozenConfigDict versions of dictionary values. Lists which have
        been converted to tuples and sets to frozensets are also stored in
        visit_map to preserve the reference structure of initial_configdict.
        visit_map need not contain (id(initial_configdict), seed) as a key/value
        pair.

  Raises:
    ValueError: If one of the following, both of which can never happen in
        practice:
            1) seed is not an empty FrozenConfigDict.
            2) initial_configdict contains a FieldReference.
  """
  # These should be impossible to raise, since the public call-site in
  # __init__() pass in valid input, as does this method recursively.
  assert isinstance(seed, FrozenConfigDict)
  assert not seed

  # This is where we define self._configdict for the FrozenConfigDict() class.
  # It is defined here instead of in FrozenConfigDict.__init__() because we must
  # fill in an empty FrozenConfigDict but do not want to have an unexpected
  # signature for FrozenConfigDict.__init__() by passing it initial_configdict.
  object.__setattr__(seed, '_configdict', initial_configdict)

  visit_map = visit_map or {}
  visit_map[id(initial_configdict)] = seed

  for key, value in initial_configdict.items():
    # This should never be raised due to elimination of references by
    # ConfigDict's iteritems
    if isinstance(value, FieldReference):
      raise ValueError('Trying to initialize a FrozenConfigDict value with '
                       'a FieldReference. This should never happen, please '
                       'file a bug.')

    if id(value) in visit_map:
      value = visit_map[id(value)]
    elif (isinstance(value, ConfigDict) and
          not isinstance(value, FrozenConfigDict)):
      value_frozenconfigdict = FrozenConfigDict(type_safe=value.is_type_safe)
      _frozenconfigdict_fill_seed(value_frozenconfigdict, value, visit_map)
      value = value_frozenconfigdict

    seed._frozen_setattr(key, value,  # pylint:disable=protected-access
                         visit_map)

