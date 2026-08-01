
def backup_keys(node: tp.Any, /, *, graph: bool | None = None):
  backups: list[StreamBackup] = []
  for _, stream in graphlib.iter_graph(node, graph=graph):
    if isinstance(stream, RngStream):
      backups.append((stream, stream.key[...]))
  return backups

