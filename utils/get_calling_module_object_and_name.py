import sys

def get_calling_module_object_and_name() -> _ModuleObjectAndName:
  """Returns the module that's calling into this module.

  We generally use this function to get the name of the module calling a
  DEFINE_foo... function.

  Returns:
    The module object that called into this one.

  Raises:
    AssertionError: Raised when no calling module could be identified.
  """
  for depth in range(1, sys.getrecursionlimit()):
    # sys._getframe is the right thing to use here, as it's the best
    # way to walk up the call stack.
    globals_for_frame = sys._getframe(depth).f_globals  # pylint: disable=protected-access
    module = get_module_object_and_name(globals_for_frame)
    if module is not None and id(module.module) not in disclaim_module_ids:
      return module
  raise AssertionError('No module was found')

