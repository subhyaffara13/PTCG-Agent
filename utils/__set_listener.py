
def _SetListener(self, listener):
  if listener is None:
    self._listener = message_listener_mod.NullMessageListener()
  else:
    self._listener = listener

