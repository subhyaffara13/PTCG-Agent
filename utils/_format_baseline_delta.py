
def _format_baseline_delta(d: baseline_lib.MetricDelta) -> str:
  """Formats one baseline metric delta as a single report line.

  Args:
    d: The metric delta to render.

  Returns:
    A line with baseline/current values, plus the speedup ratio when defined.
  """
  line = f"  {d.key}: baseline={d.baseline:.4f} current={d.current:.4f}"
  if d.ratio is not None:
    line += f" ratio={d.ratio:.3f}x"
  return line

