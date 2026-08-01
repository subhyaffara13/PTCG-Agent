
def _init_proxy_trackers(tracer: PythonKeyTracer | _GraphAppendingTracerEx) -> None:
    """Initialize the tracker dictionaries shared by PythonKeyTracer and _GraphAppendingTracerEx."""
    tracer.tensor_tracker = WeakTensorKeyDictionary()
    tracer.symnode_tracker = _SymNodeDict()
    tracer.script_object_tracker = WeakIdKeyDictionary(dict=None, ref_type=_WeakHashRef)
    tracer.opaque_tracker = WeakIdKeyDictionary()
    tracer._opaque_real_obj_proxy = {}
    tracer.sympy_expr_tracker = {}
    # Stores the torch function that was called during tracing
    tracer.torch_fn_metadata = None
    # Stores the counts for every torch function called. This is to help
    # distinguish between different calls to the same torch function.
    tracer.torch_fn_counts = {}
    tracer.enable_thunkify = False

