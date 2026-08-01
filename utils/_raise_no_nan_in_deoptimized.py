
def _raise_no_nan_in_deoptimized(e) -> NoReturn:
  msg = (f"{str(e)}. Because "
        "jax_config.debug_nans.value and/or config.jax_debug_infs is set, the "
        "de-optimized function (i.e., the function as if the `jit` "
        "decorator were removed) was called in an attempt to get a more "
        "precise error message. However, the de-optimized function did not "
        "produce invalid values during its execution. This behavior can "
        "result from `jit` optimizations causing the invalid value to be "
        "produced. It may also arise from having nan/inf literals as "
        "inputs or outputs, like `jax.jit(lambda ...: jax.numpy.nan)(...)`. "
        "\n\n"
        "It may be possible to avoid the invalid value by removing the "
        "`jit` decorator, at the cost of losing optimizations. "
        "\n\n"
        "If you see this error, consider opening a bug report at "
        "https://github.com/jax-ml/jax.")
  raise FloatingPointError(msg) from None

