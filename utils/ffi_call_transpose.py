
def ffi_call_transpose(*args, target_name, **_):
  del args
  raise ValueError(
      f"The FFI call to `{target_name}` cannot be differentiated. "
      "You can use `jax.custom_jvp` or `jax.custom_jvp` to add support.")

