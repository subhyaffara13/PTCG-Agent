
def interruptible(inner: Iterable[_T] | Iterator[_T]) -> Iterator[_T]:
  """Catch KeyboardInterrupts to end the loop without raising an Exception.

  While this iterator is running, the first SIGINT (e.g. from interrupting
  the colab runtime, or pressing Ctrl+C ) will not raise an exception but
  instead end the loop after the current iteration.
  A second SIGINT will raise a KeyboardInterrupt Exception as usual.

  Examples:

  ```python
  for i in interruptible(range(10)):
    print(i)
    time.sleep(3)
  ```

  Args:
    inner: arbitrary iterable or iterator

  Yields:
    elements from inner
  """
  interrupted = threading.Event()

  def handler(unused_signum, unused_frame):
    if interrupted.is_set():
      raise KeyboardInterrupt
    interrupted.set()

  previous_handler = signal.signal(signal.SIGINT, handler)

  try:
    for i in inner:
      yield i
      if interrupted.is_set():
        return
  finally:
    signal.signal(signal.SIGINT, previous_handler)

