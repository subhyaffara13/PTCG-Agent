import json
from typing import Any

def render_configuration(
    benchmark_name: str,
    benchmark_options: dict[str, Any] | None,
    checkpoint_config: dict[str, Any] | None,
) -> str:
  """Renders the run configuration as readable markdown.

  Options and checkpoint_config become field/value tables; any nested dict in
  checkpoint_config (typically `spec`) becomes its own fenced-JSON block.

  Args:
    benchmark_name: Title rendered as the top-level heading.
    benchmark_options: Flat option name/value pairs, or None to omit.
    checkpoint_config: Checkpoint config; scalars form a table and nested dicts
      each become a fenced-JSON block.

  Returns:
    The configuration rendered as a markdown string.
  """
  lines = [f"## {benchmark_name}", ""]

  def _table(title: str, items: list[tuple[str, Any]]) -> None:
    lines.append(f"### {title}")
    lines.append("")
    lines.append("| field | value |")
    lines.append("|---|---|")
    for k, v in items:
      lines.append(f"| `{k}` | `{v}` |")
    lines.append("")

  if benchmark_options:
    _table(
        "Benchmark options",
        [(k, v) for k, v in sorted(benchmark_options.items())],
    )

  if checkpoint_config:
    scalar_items = []
    nested_items = []
    for k, v in sorted(checkpoint_config.items()):
      if isinstance(v, dict):
        nested_items.append((k, v))
      else:
        scalar_items.append((k, v))
    if scalar_items:
      _table("Checkpoint config", scalar_items)
    for k, v in nested_items:
      lines.append(f"### Checkpoint config — `{k}`")
      lines.append("")
      lines.append("```json")
      lines.append(json.dumps(v, indent=2, sort_keys=True))
      lines.append("```")
      lines.append("")
  return "\n".join(lines)

