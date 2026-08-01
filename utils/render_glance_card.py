
def render_glance_card(
    benchmark_name: str,
    aggregates: dict[str, dict[str, float]],
    per_host_values: list[tuple[int, dict[str, float]]],
    inventory: Any | None,
    manifest: Any | None,
) -> str:
  """Quick-glance headline card: a few generic rows + per-host + inventory.

  The headline rows are candidate-key lookups whose lists cover both load and
  save tags, so the renderer needs no per-kind template: a load card's metrics
  populate the load candidates, a save card's the save candidates, and only the
  resolved ones render. The per-host byte rows (and each host's share of the
  on-disk size) are the sharding check: each host should move only its slice.
  The full per-stage breakdown lives in the `aggregated_metrics` card; the
  inventory and run manifest are appended here for provenance.

  Args:
    benchmark_name: Title rendered as the top-level heading.
    aggregates: Cross-host aggregate stats per metric key (already sliced to one
      operation name, so keys are bare tags).
    per_host_values: (host_index, metric->mean) per host, sorted by index.
    inventory: Optional directory inventory; supplies on-disk total bytes, file
      count, small-file canary, and format breakdown.
    manifest: Optional suite run manifest; appended via `as_markdown()`.

  Returns:
    The card rendered as a markdown string.
  """
  on_disk_gb = None
  if inventory is not None and getattr(inventory, "total_bytes", 0):
    on_disk_gb = inventory.total_bytes / (1024**3)
  lines = [
      f"## {benchmark_name} — at a glance",
      "",
      "| metric | value |",
      "|---|---:|",
  ]
  total = _glance_agg(aggregates, _TOTAL_TIME_KEYS, "max")
  lines.append(f"| Total time | {_glance_num(total)} s |")
  throughput = _glance_agg(aggregates, _THROUGHPUT_KEYS, "max")
  if throughput is not None:
    lines.append(f"| Throughput | {_glance_num(throughput)} GiB/s |")
  bytes_per_host = _glance_agg(aggregates, _BYTES_KEYS, "mean")
  if bytes_per_host is not None:
    lines.append(f"| Bytes / host (mean) | {_humanize_gib(bytes_per_host)} |")
  if on_disk_gb is not None:
    lines.append(f"| Checkpoint size (on-disk) | {_humanize_gib(on_disk_gb)} |")
  hbm = _glance_agg(aggregates, ["7_memory/device_hbm_peak_diff_gb"], "max")
  if hbm is not None:
    lines.append(f"| HBM peak / host (max) | {_humanize_gib(hbm)} |")
  lines.append("")
  lines += _per_host_table(
      per_host_values, _PER_HOST_COLS, pct_keys=_BYTES_KEYS, pct_of=on_disk_gb
  )
  lines += _glance_inventory(inventory)
  if manifest is not None:
    lines.append(manifest.as_markdown())
  return "\n".join(lines).rstrip() + "\n"

