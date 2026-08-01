
def _format_params(d, as_game=False):
  """Format a collection of params."""

  def fmt(val):
    if isinstance(val, dict):
      return _format_params(val, as_game=True)
    else:
      return _escape(str(val))

  if as_game:
    return d["name"] + "(" + ",".join(
        "{}={}".format(key, fmt(value))
        for key, value in sorted(d.items())
        if key != "name") + ")"
  else:
    return "{" + ",".join(
        "{}={}".format(key, fmt(value))
        for key, value in sorted(d.items())) + "}"


def _format_params(cmd: Command) -> str:
    """Format required params: positional as UPPER_CASE, options as ``--name TYPE``."""
    parts = []
    for p in cmd.params:
        if not p.required or p.human_readable_name == "--help":
            continue
        if p.name and p.name.startswith("_"):
            continue
        long_name = next((o for o in getattr(p, "opts", []) if o.startswith("--")), None)
        if long_name is not None:
            type_name = _type_hint(p)
            parts.append(f"{long_name} {type_name}")
        elif p.name:
            parts.append(p.human_readable_name)
    return " ".join(parts)

