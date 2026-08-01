
def load_arrayvis_javascript() -> str:
  """Loads the contents of `arrayvis.js` from the Python package.

  Returns:
    Source code for arrayviz.
  """
  filepath = __file__
  if filepath is None:
    raise ValueError("Could not find the path to arrayviz.js!")

  # Look for the resource relative to the current module's filesystem path.
  base = filepath.removesuffix("arrayviz_impl.py")
  load_path = os.path.join(base, "js", "arrayviz.js")

  with open(load_path, "r", encoding="utf-8") as f:
    return f.read()

