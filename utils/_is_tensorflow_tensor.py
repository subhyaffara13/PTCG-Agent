
def _is_tensorflow_tensor(external_array):
  t = type(external_array)
  return (
      t.__qualname__ == "EagerTensor"
      and t.__module__.endswith("tensorflow.python.framework.ops")
  )

