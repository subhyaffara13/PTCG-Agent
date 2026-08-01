
def _metrics_file_exists(metrics_item_path: epath.Path) -> bool:
  """True if item directory AND actual file both exist."""
  return (
      metrics_item_path.exists()
      and (metrics_item_path / METRIC_ITEM_NAME).exists()
  )

