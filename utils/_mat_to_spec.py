
def _mat_to_spec(mesh, mat):
  return P(order_wrt_mesh(mesh, mat.varying), unreduced=mat.unreduced,
           reduced=mat.reduced)

