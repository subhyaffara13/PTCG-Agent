
def _obj_html_repr(obj: object, *, array_values: bool = False) -> str:
  """Returns the object representation."""
  if isinstance(obj, type(None)):
    type_ = 'null'
  elif isinstance(obj, type(...)):
    type_ = 'null'
  elif isinstance(obj, (int, float)):
    type_ = 'number'
  elif isinstance(obj, bool):
    type_ = 'boolean'
  elif isinstance(obj, str):
    type_ = 'string'
    obj = _truncate_long_str(obj, expand_new_lines=True)
  elif isinstance(obj, bytes):
    type_ = 'string'
    obj = _truncate_long_str(repr(obj))
  elif not array_values and isinstance(obj, enp.lazy.LazyArray):
    type_ = 'number'
    obj = enp.ArraySpec.from_array(obj)
  elif isinstance(obj, attrs.ExceptionWrapper):
    type_ = 'error'
    obj = obj.e
  else:
    type_ = 'preview'
    try:
      obj = repr(obj)
    except Exception as e:  # pylint: disable=broad-except
      return _obj_html_repr(attrs.ExceptionWrapper(e))
    obj = _truncate_long_str(obj)

  if not isinstance(obj, str):
    obj = repr(obj)
    obj = html.escape(obj)
  return H.span(class_=[type_])(obj)

