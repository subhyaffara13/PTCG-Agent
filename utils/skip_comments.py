
def skip_comments(lines):
  state = 0
  for line in lines:
    n = len(line)
    l = ''
    p = 0
    while p < n:
      if state == 0:
        a = line.find('//', p)
        b = line.find('/*', p)
        if a > -1 and (a < b or b == -1):
          l += line[p:a]
          p = n
        elif b > -1 and (b < a or a == -1):
          l += line[p:b]
          p = b+2
          state = 1
        else:
          l += line[p:]
          p = n
      elif state == 1:
        a = line.rfind('*/', p)
        if a == -1:
          p = n
        else:
          p = a + 2
          state = 0
    yield l

