
def StripContentBetweenTags(filename, strip_begin_tag, strip_end_tag):
  """Strip contents from a file.

  Rewrites filename with by removing all content between
  strip_begin_tag and strip_end_tag, including the tags themselves.

  Args:
    filename: the filename to perform the replacement on
    strip_begin_tag: the start of the content to be removed
    strip_end_tag: the end of the content to be removed

  Raises:
    Exception: A failure occurred
  """
  f = open(filename, 'r')
  content = f.read()
  f.close()

  while True:
    begin = content.find(strip_begin_tag)
    if begin == -1:
      break
    end = content.find(strip_end_tag, begin + len(strip_begin_tag))
    if end == -1:
      raise Exception('{}: imbalanced strip begin ({}) and '
                      'end ({}) tags'.format(filename, strip_begin_tag,
                                             strip_end_tag))
    content = content.replace(content[begin:end + len(strip_end_tag)], '')

  f = open(filename, 'w')
  f.write(content)
  f.close()

