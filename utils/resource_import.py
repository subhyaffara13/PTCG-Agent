from typing import Optional

def resource_import(
    filename: str,
    *,
    module: Optional[epath.PathLike] = None,
) -> str:
  """Returns the `HTML` associated with the resource.

  Args:
    filename: Path to the `.css`, `.js` resource
    module: Python module name from which the filename is relative too.
  """
  path = epath.resource_path(module) if module else _static_path()
  path = path.joinpath(filename)
  content = path.read_text()
  if path.suffix == '.css':
    return f'<style>{content}</style>'
  elif path.suffix == '.js':
    return f'<script>{content}</script>'
  else:
    raise ValueError('')

