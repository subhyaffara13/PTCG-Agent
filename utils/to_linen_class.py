
def to_linen_class(
    base_nnx_class: type[M],
    base_metadata_fn: tp.Callable[[variablelib.VariableState], tp.Any] | None = bv.to_linen_var,
    base_skip_rng: bool = False,
    **partial_kwargs: tp.Any,
) -> type[ToLinen]:
  """Dynamically wraps an NNX module class into a Flax Linen module class."""

  class ToLinenPartial(ToLinen):
    """A dynamically created Linen Module that wraps a specific NNX Module.

    This class is not meant to be used directly. Instead, it is created and
    returned by the `to_linen_class` function. It acts as a "partially applied"
    version of the `ToLinen` wrapper, where the NNX module to be wrapped and
    its default arguments are pre-configured.

    When you instantiate this class, it behaves like a standard Linen module.
    The arguments you provide during instantiation can override the defaults
    that were set when this class was created by `to_linen_class`.

    For example:
      >>> from flax import linen as nn, nnx
      >>> from maxtext.src.maxtext.layers import linears
      >>> # Create a specialized Linen wrapper for linears.DenseGeneral
      >>> LinenDenseGeneral = to_linen_class(linears.DenseGeneral)
      >>> # Now, LinenDenseGeneral can be used like a regular Linen module
      >>> class MyModel(nn.Module):
      ...   def setup(self):
      ...     # Instantiate the wrapped linears.DenseGeneral with its arguments
      ...     self.dense = LinenDenseGeneral(
      ...         in_features_shape=10, out_features_shape=5
      ...     )
      ...   def __call__(self, x):
      ...     return self.dense(x)

    Attributes:
      (The attributes are dynamically set by the `ToLinen` parent class based
       on the arguments provided during instantiation.)
    """

    def __init_subclass__(cls, **kwargs):
      super().__init_subclass__(**kwargs)

      def __init__(
          self,
          args=None,
          kwargs=None,
          nnx_class=None,
          skip_rng=None,
          metadata_fn=None,
          name=_MISSING,
          parent=_MISSING,
          **other_kwargs,
      ):
        linen_kwargs = {}
        if not isinstance(parent, _Missing):
          linen_kwargs["parent"] = parent
        if not isinstance(name, _Missing):
          linen_kwargs["name"] = name
        ToLinen.__init__(
            self,
            nnx_class=nnx_class or base_nnx_class,
            args=args or (),
            metadata_fn=metadata_fn or base_metadata_fn,
            skip_rng=skip_rng or base_skip_rng,
            kwargs=FrozenDict({**partial_kwargs, **(kwargs or {}), **other_kwargs}),
            **linen_kwargs,
        )

      cls.__init__ = __init__

  return ToLinenPartial

