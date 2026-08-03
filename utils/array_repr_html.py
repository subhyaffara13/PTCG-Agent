from typing import Any, Optional

def array_repr_html(
    array: Array,
    **kwargs: Any,
) -> Optional[str]:
  """Returns the HTML `<img/>` repr, or `None` if array is not an image."""
  try:
    return _array_repr_html_inner(array, **kwargs)
  except Exception:
    # IPython display silence exceptions, so display it here
    traceback.print_exc()
    raise

