
def filter_lcov_trace(lines):
  nrs = set()
  for line in lines:
    if line.startswith('SF:'):
      nrs = set(cond_lines_from_file(line[3:-1]))
    elif line.startswith('BRDA:'):
      xs = line[5:].split(',')
      nr = int(xs[0]) if xs else 0
      if nr not in nrs:
        continue
    yield line

