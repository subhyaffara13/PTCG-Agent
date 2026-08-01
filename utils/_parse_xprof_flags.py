
def _parse_xprof_flags(unknown_flags: list[str]) -> dict[str, Any]:
  parsed: dict[str, Any] = {}
  i = 0
  while i < len(unknown_flags):
    arg = unknown_flags[i]
    if not arg.startswith('--'):
      raise ValueError(f"Unknown positional argument encountered: {arg}")

    key = arg[2:]
    if "=" in key:
      key, value_str = key.split("=", 1)
      i += 1
    elif i + 1 < len(unknown_flags) and not unknown_flags[i + 1].startswith('--'):
      value_str = unknown_flags[i + 1]
      i += 2
    else:
      parsed[key] = True
      i += 1
      continue

    value_lower = value_str.lower()
    if value_lower in {'true', 't', 'yes', 'y'}:
      parsed[key] = True
    elif value_lower in {'false', 'f', 'no', 'n'}:
      parsed[key] = False
    else:
      try:
        parsed[key] = int(value_str, 0)
      except ValueError:
        parsed[key] = value_str  # Keep as string
  return parsed

