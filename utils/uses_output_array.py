
def uses_output_array(f):
    return skip_xp_backends("dask.array", reason="output=array requires buffer view")(
        skip_xp_backends("jax.numpy", reason="output=array requires buffer view")(f))

