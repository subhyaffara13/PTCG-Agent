import os

def evaluate_platform_supports_flash_attention():
    if TEST_WITH_ROCM:
        arch_list = ["gfx90a", "gfx942", "gfx1100", "gfx1201", "gfx950"]
        if os.environ.get("TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL", "0") != "0":
            arch_list += ["gfx1101", "gfx1102", "gfx1150", "gfx1151", "gfx1200"]
        return evaluate_gfx_arch_within(arch_list)
    if TEST_CUDA:
        return not IS_WINDOWS and SM80OrLater
    if TEST_XPU:
        return True
    return False


def evaluate_platform_supports_flash_attention():
    if TEST_XPU:
        return not IS_WINDOWS and Xe2_Or_Later
    return False

