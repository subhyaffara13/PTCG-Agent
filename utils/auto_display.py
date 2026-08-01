
def auto_display(activate: bool = True) -> None:
  r"""Activate auto display statements ending with `;` (activated by default).

  Add a trailing `;` to any statement (assignment, expression, return
  statement) to display the current line.
  This call `IPython.display.display()` for pretty display.

  This change the default IPython behavior where `;` added to the last statement
  of the cell still silence the output.

  ```python
  x = my_fn();  # Display `my_fn()`

  my_fn();  # Display `my_fn()`
  ```

  `;` behavior can be disabled with `ecolab.auto_display(False)`

  Format:

  *   `my_obj;`: Alias for `IPython.display.display(x)`
  *   `my_obj;s`: (`spec`) Alias for
      `IPython.display.display(etree.spec_like(x))`
  *   `my_obj;i`: (`inspect`) Alias for `ecolab.inspect(x)`
  *   `my_obj;a`: (`array`) Alias for `media.show_images(x)` /
      `media.show_videos(x)` (`ecolab.auto_plot_array` behavior)
  *   `my_obj;p`: (`pretty_display`) Alias for `print(epy.pretty_repr(x))`.
      Can be combined with `s`. Used for pretty print `dataclasses` or print
      strings containing new lines (rather than displaying `\n`).
  *   `my_obj;h`: (`syntax_highlight`) Add Python code syntax highlighting (
      using `ecolab.highlight_html`)
  *   `my_obj;q`: (`quiet`) Don't display the line (e.g. last line)
  *   `my_obj;l`: (`line`) Also display the line (can be combined with previous
      statements). Has to be at the end (`;sl` is valid but not `;ls`).

  `p`, `s`, `h`, `l` can be combined.

  A functional API exists:

  ```python
  ecolab.disp(obj, mode='sp')  # Equivalent to `obj;sp`
  ```

  Args:
    activate: Allow to disable `auto_display`
  """

  if not epy.is_notebook():  # No-op outside Colab
    return

  # Register the transformation
  ip = IPython.get_ipython()
  shell = ip.kernel.shell

  # Clear previous transformation to support reload and disable.
  _clear_transform(shell.ast_transformers)
  if _IS_LEGACY_API:
    _clear_transform(shell.input_transformer_manager.python_line_transforms)
    _clear_transform(shell.input_splitter.python_line_transforms)
  else:
    _clear_transform(ip.input_transformers_post)

  if not activate:
    return

  # Register the transformation.
  # The `ast` do not contain the trailing `;` information, and there's no way
  # to access the original source code from `shell.ast_transformers`, so
  # the logic has 2 steps:
  # 1) Record the source code string using `python_line_transforms`
  # 2) Parse and add the `display` the source code with `ast_transformers`

  lines_recorder = _RecordLines()

  if _IS_LEGACY_API:
    _append_transform(
        shell.input_splitter.python_line_transforms, lines_recorder
    )
    _append_transform(
        shell.input_transformer_manager.python_line_transforms, lines_recorder
    )
  else:
    _append_transform(ip.input_transformers_post, lines_recorder)
  _append_transform(
      shell.ast_transformers, _AddDisplayStatement(lines_recorder)
  )

