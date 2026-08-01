
def _format_tag_attributes(attrs: dict[str, str | list[str]]) -> str:
  """Format the tag attributes."""
  out = ['']
  for k, v in attrs.items():
    if v is None:
      continue
    if k == 'class_':  # `class` is a forbidden Python keyword for arg name
      k = 'class'

    if isinstance(v, str):
      v = v.split()
    elif not isinstance(v, list):
      raise TypeError(f'Unexpected attribute: {k}={v!r}')

    # To avoid collisions, we prefix all classes with `etils-`
    if k == 'class':
      v = [f'etils-{v_}' for v_ in v]

    v = ' '.join(v)

    out.append(f'{k}="{v}"')
  return ' '.join(out)

