
def _param_rrefs(module_rref, recurse) -> list[rpc.RRef[Parameter]]:
    ret: list[rpc.RRef[Parameter]] = [
        rpc.RRef(param) for param in module_rref.local_value().parameters(recurse)
    ]
    return ret

