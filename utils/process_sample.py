
def process_sample(sample: dict[str, jax.Array]) -> dict[str, jax.Array]:
  """Converts the image to float32 and normalizes it."""
  return {
      'image': sample['image'].astype(np.float32) / 255.0,
      'label': sample['label'],
  }

