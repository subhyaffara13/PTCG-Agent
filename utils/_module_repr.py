
def _module_repr(module: 'Module', num_spaces: int = 4):
  """Returns a pretty printed representation of the module."""
  cls = type(module)
  try:
    fields = dataclasses.fields(cls)
  except TypeError:
    # Edge case with no fields e.g. module = nn.Module() causes error later.
    return object.__repr__(module)
  cls_name = cls.__name__
  rep = ''

  attributes = {
    f.name: f.type
    for f in fields
    if f.name not in ('parent', 'name') and f.repr
  }
  child_modules = {
    k: v
    for k, v in module._state.children.items()  # pytype: disable=attribute-error
    if isinstance(v, Module)
  }
  if attributes:
    rep += '# attributes\n'
    for attr in attributes.keys():
      # TODO(jheek): can we get a nice string representation of attribute types?
      value = module.__dict__.get(attr, None)
      value_rep = _attr_repr(value)
      rep += f'{attr} = {value_rep}\n'
  if child_modules:
    rep += '# children\n'
    for name, child in child_modules.items():
      child_rep = _module_repr(child, num_spaces)
      rep += f'{name} = {child_rep}\n'
  if rep:
    return f'{cls_name}(\n{_indent(rep, num_spaces)})'
  else:
    return f'{cls_name}()'

