import re

def _code_to_filename(code: types.CodeType) -> str | None:
  """Returns the canonicalized filename of a code object.

  Returns None if the filename should be omitted in tracebacks.
  """
  if not source_info_util.is_user_filename(code.co_filename):
    return None
  pattern = config.hlo_source_file_canonicalization_regex.value
  return re.sub(pattern, '', code.co_filename) if pattern else code.co_filename

