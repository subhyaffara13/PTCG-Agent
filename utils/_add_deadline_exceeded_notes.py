
def _add_deadline_exceeded_notes(e: jax.errors.JaxRuntimeError):
  """Adds notes to the exception to help debug the deadline exceeded error."""
  e.add_note('1. Make sure that the job and storage are colocated.')
  e.add_note(
      '2. Make sure that the job has enough compute resources allocated.'
  )
  e.add_note('3. Make sure that the storage has enough throughput quota.')

