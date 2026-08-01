
def dim_as_value_impl(dim: DimSize):
  raise NotImplementedError(
      "Evaluation rule for 'dim_as_value' is not implemented. "
      "It seems that you are using shape polymorphism outside jax.export.")

