
def _has_update_rule(obj):
  return isinstance(obj, (type, types.MethodType, types.FunctionType, property))

