import functools

def _reraise_error(fn: _T) -> _T:
  @functools.wraps(fn)
  def decorated(self, node: ast.AST):
    try:
      return fn(self, node)  # pytype: disable=wrong-arg-types
    except Exception as e:  # pylint: disable=broad-exception-caught
      code = '\n'.join(self.lines_recorder.last_lines)
      print(f'Error for code:\n-----\n{code}\n-----')
      traceback.print_exception(e)

  return decorated

