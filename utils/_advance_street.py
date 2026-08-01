
def _advance_street(ps: ParseState) -> None:
  ps.prev_street_max = ps.table_max
  ps.table_max = 0
  ps.contrib_street = [0 for _ in ps.contrib_street]

