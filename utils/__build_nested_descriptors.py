
def _BuildNestedDescriptors(module, msg_des, prefix):
  for name, nested_msg in msg_des.nested_types_by_name.items():
    module_name = prefix + name.upper()
    module[module_name] = nested_msg
    _BuildNestedDescriptors(module, nested_msg, module_name + '_')
  for enum_des in msg_des.enum_types:
    module[prefix + enum_des.name.upper()] = enum_des

