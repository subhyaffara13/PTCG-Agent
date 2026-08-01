
def is_pytree_checkpoint_complete(directory):
  return (directory / STATE_CHECKPOINTABLE_KEY / 'manifest.ocdbt').exists()

