
def get_async_engine(config: tiering_service_pb2.ServerConfig) -> AsyncEngine:
  """Returns an AsyncEngine configured from ServerConfig."""
  input_url = config.db_connection_str

  # Make sure we are using the async version of the driver
  if input_url.startswith("psql://"):
    url = input_url.replace("psql://", "postgresql+asyncpg://", 1)
  elif input_url.startswith("sqlite://"):
    url = input_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
  else:
    url = input_url
  return create_async_engine(url)

