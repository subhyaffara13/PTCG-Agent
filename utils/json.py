import uuid

def json(value: Json, expanded: bool = False) -> None:
  """Display the Json `dict` / `list` interactivelly (with collapsible elems).

  Examples:

  ```python
  ecolab.json({'a': [1, 2, 3], 'b': {'x': True, 'y': False}})
  ```

  The dict keys and list indices can be filtered from the display field using
  regex (e.g. `a.[0-9]` in the above example).

  Args:
    value: Json `dict` or `list` to inspect.
    expanded: Whether the elements start as expanded or as collapsed.
  """
  # Unique id to make sure multiple Json display do not interact with each other
  id_ = uuid.uuid1().hex

  # There are a lot of alternative to `alenaksu/json-viewer`.
  # Likely the most popular one is `react-json-view`. However, this one
  # display preview for collapsible elements, which is nice (and not present
  # in other alternatives).
  # https://github.com/mac-s-g/react-json-view/issues/237

  css_content = """
  json-viewer {
    padding:1px 1.5em 1px 1.5em;
    --background-color: #f7f7f7;
    --property-color: #087db2;
    --string-color: #a31515;
    --number-color: #008000;
    --boolean-color: #0000ff;
    --null-color: #af00db;
    --preview-color: #888888;
  }
  json-viewer::part(key) {
    margin-right: 0.5em;
  }
  html[theme=dark] json-viewer {
    --background-color: #2c2c2c;
    --property-color: #6fb3d2;
    --string-color: #ce9178;
    --number-color: #b5cea8;
    --boolean-color: #569cd6;
    --null-color: #c586c0;
    --preview-color: #888888;
  }
  .ecolab-json button {
      background-color: var(--colab-highlighted-surface-color);
      color: var(--colab-primary-text-color);
      border-width: 0;
  }
  .ecolab-json input {
      border-color: var(--colab-highlighted-surface-color);
  }
  """

  html_content = html.escape(json_std.dumps(value))
  # if expanded is True, call viewer.expandAll()
  expand_line = f'viewer{id_}.expandAll();\n' if expanded else ''
  html_content = f"""
  <script src="https://unpkg.com/@alenaksu/json-viewer@2.0.0/dist/json-viewer.bundle.js"></script>
  <script>
    const viewer{id_} = document.querySelector('#json{id_}');
    {expand_line}
  </script>
  <style>
  {css_content}
  </style>
  <div class="ecolab-json">
    <button onclick="viewer{id_}.expandAll();">Expand All</button>
    <button onclick="viewer{id_}.collapseAll();">Collapse All</button>
    <input placeholder="Filter Regex" onkeyup="viewer{id_}.filter(RegExp(this.value, 'i'));"></input>
    <json-viewer id="json{id_}">{html_content}</json-viewer>
  </div>
  """
  IPython.display.display(IPython.display.HTML(html_content))

