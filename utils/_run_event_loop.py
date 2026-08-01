
def _run_event_loop(loop: asyncio.AbstractEventLoop) -> None:
  """Runs the event loop until stop() is called."""
  loop.run_forever()
  loop.close()

