
def GccStyleFilterAndCombine(default_flags, test_flags):
  """Merges default_flags and test_flags for GCC and LLVM.

  Args:
    default_flags: A list of default compiler flags
    test_flags: A list of flags that are only used in tests

  Returns:
    A combined list of default_flags and test_flags, but with all flags of the
    form '-Wwarning' removed if test_flags contains a flag of the form
    '-Wno-warning'
  """
  remove = set(["-W" + f[5:] for f in test_flags if f[:5] == "-Wno-"])
  return [f for f in default_flags if f not in remove] + test_flags

