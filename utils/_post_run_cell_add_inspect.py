
def _post_run_cell_add_inspect(*args) -> None:
  """Callback after cell execution to add the `inspect` button."""
  del args  # Future version of IPython will have a `result` arg

  # TODO(epot): Detect if IPython has output
  # Currently, this add an output because `_` is set to the previous
  # value if no output is set.
  ip = IPython.get_ipython()

  # TODO(epot): Store the `last_result` in a weakref to avoid memory leaks.
  last_result = ip.ev('_')
  root = nodes.Node.from_obj(last_result)

  # TODO(epot): Should not load all `css`/`js` everytime ?
  # Especially the main inspect one which is used only after activation.
  html_content = IPython.display.HTML(f"""
      {pyjs_com.js_import()}
      {resource_utils.resource_import('auto_activate.css')}
      {resource_utils.resource_import('auto_activate.js')}
      {resource_utils.resource_import('theme.css')}
      {resource_utils.resource_import('main.js')}

      <script>
        add_auto_activate("{root.id}");
      </script>
  """)
  IPython.display.display(html_content)

