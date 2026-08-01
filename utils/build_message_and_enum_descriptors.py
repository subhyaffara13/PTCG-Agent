
def BuildMessageAndEnumDescriptors(file_des, module):
  """Builds message and enum descriptors.

  Args:
    file_des: FileDescriptor of the .proto file
    module: Generated _pb2 module
  """
  for (name, msg_des) in file_des.message_types_by_name.items():
    module_name = '_' + name.upper()
    module[module_name] = msg_des
    _BuildNestedDescriptors(module, msg_des, module_name + '_')

