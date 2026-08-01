
def name_jvp(primals, tangents, *, name):
  (x,), (xdot,) = primals, tangents
  return name_p.bind(x, name=name), xdot  # don't name the tangent value

