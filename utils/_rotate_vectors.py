
def _rotate_vectors(H, i, cs, sn):
  x1 = H[i]
  y1 = H[i + 1]
  x2 = cs.conj() * x1 - sn.conj() * y1
  y2 = sn * x1 + cs * y1
  H = H.at[i].set(x2)
  H = H.at[i + 1].set(y2)
  return H

