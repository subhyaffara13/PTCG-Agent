
def _should_create_directories_synchronously(
    context: context_lib.Context, partial_save: bool
):
  return (
      partial_save
      or not context.async_options.create_directories_asynchronously
  )

