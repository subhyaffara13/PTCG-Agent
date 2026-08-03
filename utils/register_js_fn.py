import functools

def register_js_fn(fn: _FnT) -> _FnT:
  r"""Decorator to make a function callable from Javascript.

  Usage:

  In Python:

  ```python
  @register_js_fn
  def my_fn(*args, **kwargs):
    return {'x': 123}
  ```

  The function can then be called from Javascript:

  ```python
  # Currently has to be executed in the same cell to install the library
  IPython.display.display(IPython.display.HTML(ecolab.pyjs_import()))

  IPython.display.HTML(\"\"\"
  <script>
    async function main() {
      out = await call_python('my_fn', [1, 2], {z: 3});
      console.log(out['sum']);  // my_fn(1, 2, z=3)  == {'sum': 6}
    }
    main();
  </script>
  \"\"\")
  ```

  Note that Javascript require the `pyjs_com.js_import()` statement to be
  present in the HTML from the cell.

  Args:
    fn: The Python function, can return any json-like value or dict

  Returns:
    The Python function, unmodified
  """

  # No-op when running on tests
  if not epy.is_notebook():
    return fn

  if _is_notebook_colab():
    backend = _Colab()
  else:
    backend = _Jupyter()

  @functools.wraps(fn)
  def decorated(*args, **kwargs):
    try:
      out = fn(*args, **kwargs)
      # Wrap non-dict values inside JSON
      if not isinstance(out, dict):
        out = {'__etils_pyjs__': out}
      # Eventually wrap the output
      return backend.wrap_output(out)
    except Exception as e:
      traceback.print_exception(e)
      raise

  backend.register_fn(decorated)
  return fn

