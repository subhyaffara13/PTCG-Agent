
def js_import() -> str:
  """`<script></script>` to import to add in the HTML."""
  path = epath.resource_path('etils.ecolab') / 'pyjs_com/py_js_com.js'
  return f'<script>{path.read_text()}</script>'

