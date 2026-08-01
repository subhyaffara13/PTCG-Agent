
def script_rref_run_forward_my_script_module(rref: RRef[MyModuleInterface]) -> Tensor:
    return rref.to_here().forward()

