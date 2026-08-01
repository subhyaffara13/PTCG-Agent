
def get_kernel_launch() -> str:
    return "call_triton_" if torch._inductor.config.cpp_wrapper else ".run("

