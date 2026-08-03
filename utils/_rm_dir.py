from typing import Any

def _rm_dir(root: Any) -> None:
  if _is_remote_path(root):
    root.rmtree()
  else:
    shutil.rmtree(root)

