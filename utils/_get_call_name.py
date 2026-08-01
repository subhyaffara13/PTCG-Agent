
def _get_call_name(call: _DebugCall) -> str:
    """String identifying _DebugCall (e.g. func, kernel, module name)"""
    if isinstance(call, _OpCall):
        return _get_op_name(call.op)
    elif isinstance(call, _TritonKernelCall):
        return call.kernel_name
    elif isinstance(call, _AnnotateCall):
        return f"[{call.header}] {call.tag}"
    elif isinstance(call, _RedistributeCall):
        return REDISTRIBUTE_FUNC
    else:
        return str(call)

