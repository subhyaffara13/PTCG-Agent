
def filter_lcov_trace_file(s_filename, d_file):
  with open(s_filename) as f:
    for l in filter_lcov_trace(f):
      print(l, end='', file=d_file)

