
def cond_lines_from_file(filename):
  with open(filename) as f:
    yield from cond_lines(skip_comments(f))

