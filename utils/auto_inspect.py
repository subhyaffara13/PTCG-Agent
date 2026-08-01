
def auto_inspect() -> None:
  """Add a button on each cell outputs to switch output to `ecolab.inspect`."""
  ip_utils.register_once(
      'post_run_cell',
      _post_run_cell_add_inspect,
      '__is_auto_inspect__',
  )

