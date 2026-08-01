
def LoadedExecutable_execute(self, arguments, device=None):
  del device
  results = self.execute_sharded(arguments)
  return [x[0] for x in results.disassemble_into_single_device_arrays()]

