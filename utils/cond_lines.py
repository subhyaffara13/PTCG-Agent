
def cond_lines(lines):
  state = 0
  pcnt = 0
  for nr, line in enumerate(lines, 1):
    if not line:
      continue
    n = len(line)
    p = 0
    do_yield = False
    while p < n:
      if state == 0:
        p = line.find('if', p)
        if p == -1:
          p = n
          continue
        if (p == 0 or not line[p-1].isalpha()) \
            and (p+2 == len(line) or not line[p+2].isalpha()):
          do_yield = True
          state = 1
        p += 2
      elif state == 1:
        do_yield = True
        p = line.find('(', p)
        if p == -1:
          p = n
        else:
          p += 1
          state = 2
          pcnt = 1
      elif state == 2:
        do_yield = True
        for p in range(p, n):
          if line[p] == '(':
            pcnt += 1
          elif line[p] == ')':
            pcnt -= 1
          if not pcnt:
            state = 0
            break
        p += 1
    if do_yield:
      yield nr

