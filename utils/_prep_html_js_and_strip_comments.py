
def _prep_html_js_and_strip_comments(src):
  stream = io.StringIO()
  for line in src.splitlines():
    stripped = line.strip()
    if stripped and not stripped.startswith("//"):
      stream.write(stripped)
      stream.write(" ")
  return stream.getvalue()[:-1]

