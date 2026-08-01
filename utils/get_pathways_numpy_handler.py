
def get_pathways_numpy_handler() -> type_handlers.NumpyHandler:
  """Returns the Pathways NumpyHandler."""
  return type_handlers.NumpyHandler(ocdbt_process_id='pwcontroller')

