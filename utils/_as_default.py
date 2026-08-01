
def _as_default(summary_writer: tf.summary.SummaryWriter, auto_flush: bool):
  """No-flush variation of summary_writer.as_default()."""
  context_manager = summary_writer.as_default()
  try:
    context_manager.__enter__()
    yield summary_writer
  finally:
    old_flush = summary_writer.flush
    new_flush = old_flush if auto_flush else lambda: None
    summary_writer.flush = new_flush
    context_manager.__exit__(None, None, None)
    summary_writer.flush = old_flush

