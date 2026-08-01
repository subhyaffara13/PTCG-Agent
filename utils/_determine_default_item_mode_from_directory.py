
def _determine_default_item_mode_from_directory(step_path: epath.Path) -> bool:
  return (step_path / DEFAULT_ITEM_NAME).exists()

