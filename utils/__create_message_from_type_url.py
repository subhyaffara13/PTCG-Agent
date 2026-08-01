
def _CreateMessageFromTypeUrl(type_url, descriptor_pool):
  """Creates a message from a type URL."""
  db = symbol_database.Default()
  pool = db.pool if descriptor_pool is None else descriptor_pool
  type_name = type_url.split('/')[-1]
  try:
    message_descriptor = pool.FindMessageTypeByName(type_name)
  except KeyError as e:
    raise TypeError(
        'Can not find message descriptor by type_url: {0}'.format(type_url)
    ) from e
  message_class = message_factory.GetMessageClass(message_descriptor)
  return message_class()

