from typing import Any

def render_aggregated_metrics(
    benchmark_name: str,
    aggregated_stats_dict: dict[str, Any],
    metric_units: dict[str, str],
    host_label: str | None = None,
) -> str:
  """Renders mean/std/min/max/n/unit per metric, grouped by `/` prefix.

  The numbered section prefix (`2_save_breakdown/`, …) mirrors the
  Scalars-view navigation so a reader finds a metric the same way in both
  surfaces.

  Args:
    benchmark_name: Title rendered as the top-level heading.
    aggregated_stats_dict: Metric key -> AggregatedStats to tabulate.
    metric_units: Metric key -> unit string.
    host_label: When set, appended to the header to identify the host.

  Returns:
    The aggregated metrics rendered as a markdown string.
  """
  if not aggregated_stats_dict:
    return "_No successful runs to aggregate._"

  groups: dict[str, list[str]] = collections.defaultdict(list)
  for key in sorted(aggregated_stats_dict):
    head, _, _ = key.partition("/")
    section = head if "/" in key else "_other_"
    groups[section].append(key)

  suffix = f" — {host_label}" if host_label else ""
  lines = [f"## {benchmark_name} — aggregated metrics{suffix}", ""]
  for section in sorted(groups):
    lines.append(f"### {section}")
    lines.append("")
    lines.append("| metric | mean | ± std | min | max | n | unit |")
    lines.append("|---|---:|---:|---:|---:|---:|---|")
    for key in groups[section]:
      stats = aggregated_stats_dict[key]
      unit = metric_units.get(key, "")
      leaf = key.split("/", 1)[1] if "/" in key else key
      lines.append(
          f"| `{leaf}` | {stats.mean:.4f} | {stats.std:.4f} |"
          f" {stats.min:.4f} | {stats.max:.4f} | {stats.count} | {unit} |"
      )
    lines.append("")
  return "\n".join(lines)

