
def create_dataset(split: str, batch_size: int) -> pygrain.IterDataset:
  """Creates a Grain-based dataset for a given split."""
  """TODO(zachmeyers): parameterize seed."""  # pylint: disable=pointless-string-statement
  dataset = (
      pygrain.MapDataset.source(tfds.data_source('mnist', split=split))
      .map(process_sample)
      .seed(seed=45)
      .shuffle()
      .batch(batch_size, drop_remainder=True)
  )
  return dataset.to_iter_dataset()

