
def _strip_workspace_root(filename: str, workspace_root: str) -> str:
  i = filename.rfind(workspace_root)
  return filename[i+len(workspace_root):] if i >= 0 else filename

