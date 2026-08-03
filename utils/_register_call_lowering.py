import functools

def _register_call_lowering(platform):
  mlir.register_lowering(call_tf_p, functools.partial(_call_tf_lowering,
                                                      platform=platform),
                         platform=platform)

