
def _get_thread_id():
  """Gets id of current thread, suitable for logging as an unsigned quantity.

  If pywrapbase is linked, returns GetTID() for the thread ID to be
  consistent with C++ logging.  Otherwise, returns the numeric thread id.
  The quantities are made unsigned by masking with 2*sys.maxint + 1.

  Returns:
    Thread ID unique to this process (unsigned)
  """
  thread_id = threading.get_ident()
  return thread_id & _THREAD_ID_MASK

