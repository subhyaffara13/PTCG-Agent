
def _tabulate_context():
  _context.call_info_stack.append(_CallInfoContext(0, []))
  try:
    yield
  finally:
    _context.call_info_stack.pop()

