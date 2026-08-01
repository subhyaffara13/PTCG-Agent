
def _axis_types_dict(mesh):
  if not mesh.axis_names:
    return {}
  d = defaultdict(list)
  for n, t in safe_zip(mesh.axis_names, mesh.axis_types):
    d[t].append(n)
  return {t: tuple(n) for t, n in d.items()}

