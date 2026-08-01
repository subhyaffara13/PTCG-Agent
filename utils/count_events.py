
def count_events(event):
  "Returns a context-manager that yields a function that counts a test event."
  @contextmanager
  def count_event():
    before = thread_local_state.counts.get(event, 0)
    yield lambda: thread_local_state.counts.get(event, 0) - before
  return count_event

