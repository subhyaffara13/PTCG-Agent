
def _sycl_arch_as_compile_option() -> str:
    arc_option_map = {"Xe12": "intel_gpu_pvc", "Xe20": "intel_gpu_bmg_g21"}
    arch = get_xpu_arch()
    return arc_option_map.get(arch, "intel_gpu_pvc")

