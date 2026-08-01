
def restore_rngs(backups: tp.Iterable[StreamBackup], /):
  for backup in backups:
    stream = backup[0]
    stream.key.set_value(backup[1])
    if len(backup) == 3:
      stream.count.set_value(backup[2])  # count

