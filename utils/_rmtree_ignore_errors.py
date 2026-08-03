import os

def _rmtree_ignore_errors(path: str) -> None:
  if os.path.isfile(path):
    try:
      os.unlink(path)
    except OSError:
      pass
  else:
    shutil.rmtree(path, ignore_errors=True)

