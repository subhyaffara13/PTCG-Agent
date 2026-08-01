
def _per_host_table(
    per_host_values: list[tuple[int, dict[str, float]]],
    columns: list[tuple[str, list[str], str]],
    pct_keys: list[str] | None = None,
    pct_of: float | None = None,
) -> list[str]:
  """Renders one row per host for the columns at least one host reported.

  Args:
    per_host_values: (host_index, metric->mean) per host, sorted by index.
    columns: (column label, candidate metric keys, kind) tuples; kind is "bytes"
      (GiB value, humanized), "count" (integer), or "num" (decimal).
    pct_keys: Candidate keys whose value is shown as a percentage of `pct_of`.
    pct_of: Denominator for the percentage column; omitted when falsy.

  Returns:
    Markdown lines for the table, or empty if there is nothing to show.
  """
  present = [
      (label, keys, kind)
      for label, keys, kind in columns
      if any(_glance_host(v, keys) is not None for _, v in per_host_values)
  ]
  if not per_host_values or not present:
    return []
  show_pct = False
  if pct_keys is not None and pct_of:
    show_pct = any(
        _glance_host(v, pct_keys) is not None for _, v in per_host_values
    )
  header = "| host |" + "".join(f" {label} |" for label, _, _ in present)
  separator = "|---|" + "---:|" * len(present)
  if show_pct:
    header += " % of total |"
    separator += "---:|"
  lines = ["#### Per-host", "", header, separator]
  for idx, values in per_host_values:
    row = f"| {idx} |"
    for _, keys, kind in present:
      value = _glance_host(values, keys)
      if kind == "bytes":
        cell = _humanize_gib(value)
      elif kind == "count":
        cell = _glance_num(value, "{:.0f}")
      else:
        cell = _glance_num(value)
      row += f" {cell} |"
    if show_pct and pct_keys is not None and pct_of:
      part = _glance_host(values, pct_keys)
      row += f" {part / pct_of * 100:.1f}% |" if part is not None else " — |"
    lines.append(row)
  lines.append("")
  return lines

