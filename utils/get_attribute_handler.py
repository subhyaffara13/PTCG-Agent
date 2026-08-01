
def get_attribute_handler(type_: type[Any]) -> AttributeHandler:
  return _attribute_handlers[type_]

