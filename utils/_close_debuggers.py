
def _close_debuggers():
  for console in _web_consoles.values():
    console.close()
  _web_consoles.clear()

