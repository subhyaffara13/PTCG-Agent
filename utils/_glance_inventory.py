from typing import Any

def _glance_inventory(inventory: Any | None) -> list[str]:
  """Renders the checkpoint inventory block (folded in from the scorecard)."""
  if inventory is None:
    return []
  out = ["### Inventory", "", "| field | value |", "|---|---:|"]
  out.append(f"| total bytes | {_humanize_bytes(inventory.total_bytes)} |")
  out.append(f"| file count | {inventory.file_count:,} |")
  small_pct = inventory.small_file_pct * 100
  canary = "✓" if small_pct < 10 else "⚠ chunk_byte_size too small?"
  out.append(f"| small files <1 MiB | {small_pct:.1f}% {canary} |")
  if inventory.largest_file_bytes > 0:
    out.append(
        f"| largest file | {_humanize_bytes(inventory.largest_file_bytes)} |"
    )
  if inventory.format:
    fmt_str = ", ".join(f"{k}={v}" for k, v in sorted(inventory.format.items()))
    out.append(f"| format breakdown | {fmt_str} |")
  out.append("")
  return out

