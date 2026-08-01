
def is_jax_jitting(x):
    """returns True if we are inside of `jax.jit` context, False otherwise.

    When a torch model is being compiled with `jax.jit` using torchax,
    the tensor that goes through the model would be an instance of
    `torchax.tensor.Tensor`, which is a tensor subclass. This tensor has
    a `jax` method to return the inner Jax array
    (https://github.com/google/torchax/blob/13ce870a1d9adb2430333c27bb623469e3aea34e/torchax/tensor.py#L134).
    Here we use ducktyping to detect if the inner jax array is a jax Tracer
    then we are in tracing context. (See more at: https://github.com/jax-ml/jax/discussions/9241)

    Args:
      x: torch.Tensor

    Returns:
      bool: whether we are inside of jax jit tracing.
    """

    if not hasattr(x, "jax"):
        return False
    try:
        import jax

        return isinstance(x.jax(), getattr(jax, "core").Tracer)
    except Exception:
        return False

