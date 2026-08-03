from typing import Any

def disp(obj: Any, mode: str = '') -> None:
  """Display the object.

  This is the functional API for the `;` auto display magic.

  Args:
    obj: The object to display
    mode: Any mode supported by `ecolab.auto_display()`
  """
  if _Options.LINE in mode:
    raise NotImplementedError('Line mode not supported in `disp()`')
  # Do not return anything so the object is not displayed twice at the last
  # instuction of a cell
  _display_and_return(obj, options=mode)

