
def set_sqlite_pragma(dbapi_connection, connection_record):
  """Enables foreign key constraints on SQLite database connections.

  This is SQLite-specific because other databases (like PostgreSQL) enforce
  foreign keys by default and do not support SQLite's PRAGMA syntax.
  We perform an isinstance check against the standard sqlite3.Connection
  and SQLAlchemy's aiosqlite adapter wrapper to verify if this is an SQLite
  connection.

  Args:
    dbapi_connection: The database connection to configure.
    connection_record: Metadata about the connection.
  """
  del connection_record
  connection_types = (sqlite3.Connection, AsyncAdapt_aiosqlite_connection)

  if isinstance(dbapi_connection, connection_types):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

