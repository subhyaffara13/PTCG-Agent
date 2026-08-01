
def _as_yaml_str(value) -> str:
  if (hasattr(value, '__len__') and len(value) == 0) or value is None:
    return ''

  file = io.StringIO()
  yaml.safe_dump(
    value,
    file,
    default_flow_style=False,
    indent=2,
    sort_keys=False,
    explicit_end=False,
  )
  return file.getvalue().replace('\n...', '').replace("'", '').strip()


def _as_yaml_str(value) -> str:
  if (hasattr(value, '__len__') and len(value) == 0) or value is None:
    return ''

  value = jax.tree.map(_normalize_values, value)
  value = _maybe_pytree_to_dict(value)

  file = io.StringIO()
  yaml.dump(
    value,
    file,
    Dumper=NoneDumper,
    default_flow_style=False,
    indent=2,
    sort_keys=False,
    explicit_end=False,
  )
  return file.getvalue().replace('\n...', '').replace("'", '').strip()

