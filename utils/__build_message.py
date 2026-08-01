
def _BuildMessage(module_name, msg_des, prefix):
  create_dict = {}
  for name, nested_msg in msg_des.nested_types_by_name.items():
    create_dict[name] = _BuildMessage(
        module_name, nested_msg, prefix + msg_des.name + '.'
    )
  create_dict['DESCRIPTOR'] = msg_des
  create_dict['__module__'] = module_name
  create_dict['__qualname__'] = prefix + msg_des.name
  message_class = _reflection.GeneratedProtocolMessageType(
      msg_des.name, (_message.Message,), create_dict
  )
  _sym_db.RegisterMessage(message_class)
  return message_class

