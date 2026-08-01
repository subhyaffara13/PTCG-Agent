
def ReplaceStringsInFile(filename, replacement_dict):
  """Performs textual replacements in a file.

  Rewrites filename with the keys in replacement_dict replaced with
  their values. This function assumes the file can fit in memory.

  Args:
    filename: the filename to perform the replacement on
    replacement_dict: a dictionary of key strings to be replaced with their
      values

  Raises:
    Exception: A failure occurred
  """
  f = open(filename, 'r')
  content = f.read()
  f.close()

  for key, value in replacement_dict.items():
    original = content
    content = content.replace(key, value)
    if content == original:
      raise Exception('Failed to find {} in {}'.format(key, filename))

  f = open(filename, 'w')
  f.write(content)
  f.close()

