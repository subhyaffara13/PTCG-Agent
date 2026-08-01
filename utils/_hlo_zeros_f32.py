
def _hlo_zeros_f32(shape):
  return hlo.constant(
      ir.DenseElementsAttr.get(
          np.zeros(shape, dtype=np.float32), type=ir.F32Type.get()))

