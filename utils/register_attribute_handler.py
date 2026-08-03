from typing import Any

def register_attribute_handler(type_: type[Any], handler_fun: AttributeHandler):
  _attribute_handlers[type_] = handler_fun

