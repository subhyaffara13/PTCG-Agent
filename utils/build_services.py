
def BuildServices(file_des, module_name, module):
  """Builds services classes and services stub class.

  Args:
    file_des: FileDescriptor of the .proto file
    module_name: str, the name of generated _pb2 module
    module: Generated _pb2 module
  """
  # pylint: disable=g-import-not-at-top
  from google.protobuf import service_reflection
  # pylint: enable=g-import-not-at-top
  for (name, service) in file_des.services_by_name.items():
    module[name] = service_reflection.GeneratedServiceType(
        name, (),
        dict(DESCRIPTOR=service, __module__=module_name))
    stub_name = name + '_Stub'
    module[stub_name] = service_reflection.GeneratedServiceStubType(
        stub_name, (module[name],),
        dict(DESCRIPTOR=service, __module__=module_name))

