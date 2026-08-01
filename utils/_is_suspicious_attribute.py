
def _is_suspicious_attribute(
    testCaseClass: type[unittest.TestCase], name: str
) -> bool:
  """Returns True if an attribute is a method named like a test method."""
  if name.startswith('Test') and len(name) > 4 and name[4].isupper():
    attr = getattr(testCaseClass, name)
    if inspect.isfunction(attr) or inspect.ismethod(attr):
      args = inspect.getfullargspec(attr)
      return (len(args.args) == 1 and args.args[0] == 'self' and
              args.varargs is None and args.varkw is None and
              not args.kwonlyargs)
  return False

