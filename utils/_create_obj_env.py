
def _create_obj_env(object_types):
  "Turn a set of object types into a dictionary mapping (type, method name) pairs to methods"
  result = {}
  for obj_type in object_types:
    for name, top_method in inspect.getmembers(obj_type, inspect.isfunction):
      if not name.startswith('_') or name == '__call__':
        result[(obj_type, name)] = top_method
  return result

