
def subselect(row, keys):
  for key in keys:
    row = row[key]
  return row

