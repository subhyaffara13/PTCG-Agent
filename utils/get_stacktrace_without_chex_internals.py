
def get_stacktrace_without_chex_internals() -> List[traceback.FrameSummary]:
  """Returns the latest non-chex frame from the call stack."""
  stacktrace = list(traceback.extract_stack())
  for i in reversed(range(len(stacktrace))):
    fname = stacktrace[i].filename
    if fname.find("/chex/") == -1 or fname.endswith("_test.py"):
      return stacktrace[:i+1]

  debug_info = "\n-----\n".join(traceback.format_stack())
  raise RuntimeError(
      "get_stacktrace_without_chex_internals() failed. "
      "Please file a bug at https://github.com/deepmind/chex/issues and "
      "include the following debug info in it. "
      "Please make sure it does not include any private information! "
      f"Debug: '{debug_info}'.")

