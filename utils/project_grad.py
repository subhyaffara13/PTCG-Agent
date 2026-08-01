
def project_grad(g):
  """Project gradient onto tangent space of simplex."""
  return g - g.sum() / g.size

