from typing import Any, Callable

def nnx_to_linen(
    model_class: nnx.Module,
    sample_shape: tuple[int, ...],
    seed: int = 0,
    *args: Any,
    **kwargs: Any,
) -> tuple[Callable, nnx.bridge.ToLinen]:
  new_model = nnx.bridge.ToLinen(model_class, *args, **kwargs)
  variables = new_model.init(
      jax.random.key(seed), (1, *sample_shape), train=False
  )
  return new_model.apply, variables

