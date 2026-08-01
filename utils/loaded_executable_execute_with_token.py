
def LoadedExecutable_execute_with_token(self, arguments, device=None):
  del device
  results = self.execute_sharded(arguments, with_tokens=True)
  return (
      [x[0] for x in results.disassemble_into_single_device_arrays()],
      results.consume_token().get_token(0),
  )

