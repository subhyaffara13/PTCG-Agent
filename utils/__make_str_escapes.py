
def _MakeStrEscapes():
  ret = {}
  for i in range(0, 128):
    if not _AsciiIsPrint(i):
      ret[i] = r'\%03o' % i
  ret[ord('\t')] = r'\t'  # optional escape
  ret[ord('\n')] = r'\n'  # optional escape
  ret[ord('\r')] = r'\r'  # optional escape
  ret[ord('"')] = r'\"'  # necessary escape
  ret[ord('\'')] = r"\'"  # optional escape
  ret[ord('\\')] = r'\\'  # necessary escape
  return ret

