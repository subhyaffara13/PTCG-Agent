
def pallas_export_experimental(dynamic_shapes: bool):
  old_dynamic_shapes = _pallas_tracing_env.dynamic_shapes
  try:
    _pallas_tracing_env.dynamic_shapes = dynamic_shapes
    yield
  finally:
    _pallas_tracing_env.dynamic_shapes = old_dynamic_shapes

