
def initialize_hybrid_kernels():
  if _cuhybrid:
    _cuhybrid.initialize()
  if _hiphybrid:
    _hiphybrid.initialize()

