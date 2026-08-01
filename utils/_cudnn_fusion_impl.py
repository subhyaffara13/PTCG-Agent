
def _cudnn_fusion_impl(*args, jaxpr, **unused_kwargs):
  del unused_kwargs
  return jax_core.jaxpr_as_fun(jaxpr)(*args)

