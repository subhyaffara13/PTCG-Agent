
def visualize_array_sharding(arr, **kwargs):
  """Visualizes an array's sharding."""
  def _visualize(sharding):
    return visualize_sharding(arr.shape, sharding, **kwargs)
  inspect_array_sharding(arr, callback=_visualize)

