
def _make_events_generator(path):
  """Makes a generator yielding TensorBoard events from files in `path`."""
  return directory_watcher.DirectoryWatcher(
    path, event_file_loader.EventFileLoader, io_wrapper.IsSummaryEventsFile
  ).Load()

