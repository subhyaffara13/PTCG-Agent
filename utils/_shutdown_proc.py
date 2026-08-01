
def _shutdown_proc(p, timeout):
  """Waits for a proc to shut down; terminates or kills it after `timeout`."""
  freq = 10  # how often to check per second
  for _ in range(1 + timeout * freq):
    p.terminate()
    ret = p.poll()
    if ret is not None:
      return ret
    time.sleep(1 / freq)
  p.kill()
  return p.wait()

