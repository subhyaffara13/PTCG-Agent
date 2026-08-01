
def _PrefixWithDot(name):
  return name if name.startswith('.') else '.%s' % name

