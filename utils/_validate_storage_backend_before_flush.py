
def _validate_storage_backend_before_flush(
    mapper: sqlalchemy.orm.Mapper,
    connection: sqlalchemy.engine.Connection,
    target: StorageBackend,
) -> None:
  del mapper, connection
  target.validate_pre_commit()

