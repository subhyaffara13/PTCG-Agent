
def ranges_like(*xs):
  start = 0
  for x in xs:
    x_len = len(x)
    yield range(start, start + x_len)
    start += x_len

