
def _vma_ur_str(mat, spec_unreduced, spec_reduced, mesh):
  vma = mat.varying
  # TODO(yashkatariya): Diff between explicit unreduced and manual unreduced
  unreduced = mat.unreduced | spec_unreduced
  reduced = mat.reduced | spec_reduced
  if not vma and not unreduced and not reduced:
    return ''
  vma_str = _create_str(order_wrt_mesh(mesh, vma), 'V') if vma else ''
  ur_str = _create_str(order_wrt_mesh(mesh, unreduced), 'U') if unreduced else ''
  red_str = _create_str(order_wrt_mesh(mesh, reduced), 'R') if reduced else ''
  m_str = f"{vma_str}{ur_str}{red_str}".rstrip(', ')
  return f"{{{m_str}}}"

