
def _run_debugger(frames, thread_id, **kwargs):
  try:
    ColabDebugger(frames, thread_id, **kwargs).run()
  except Exception:
    traceback.print_exc()

