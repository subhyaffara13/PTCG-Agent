
def _web_pdb_version() -> tuple[int, ...]:
  import web_pdb  # pyrefly: ignore[missing-import]
  return tuple(map(int, web_pdb.__version__.split(".")))

