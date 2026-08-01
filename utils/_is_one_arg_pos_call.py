
def _is_one_arg_pos_call(call: nodes.NodeNG) -> bool:
    """Is this a call with exactly 1 positional argument ?"""
    return isinstance(call, nodes.Call) and len(call.args) == 1 and not call.keywords

