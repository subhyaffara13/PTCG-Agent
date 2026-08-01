
def get_bucket(bucket_name: str):
  # pylint: disable=g-import-not-at-top
  from google.cloud import storage  # pytype: disable=import-error

  client = storage.Client()
  return client.get_bucket(bucket_name)

