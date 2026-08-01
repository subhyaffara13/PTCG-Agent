
def get_pathways_scalar_handler() -> type_handlers.ScalarHandler:
  """Returns the Pathways ScalarHandler."""
  return type_handlers.ScalarHandler(ocdbt_process_id='pwcontroller')

