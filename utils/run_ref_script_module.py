
def run_ref_script_module(
    ref_script_module: RRef[MyModuleInterface], t: Tensor
) -> Tensor:
    module = ref_script_module.to_here()
    return module.forward() + t

