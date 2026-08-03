import sys

def runtime_environment() -> str | None:
  """Returns None, "bazel" or "pytest"."""
  if sys.executable is None:
    return None
  elif 'bazel-out' in sys.executable:
    return "bazel"
  else:
    return "pytest"

