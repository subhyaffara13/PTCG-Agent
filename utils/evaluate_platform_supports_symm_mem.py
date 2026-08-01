
def evaluate_platform_supports_symm_mem():
    if TEST_CUDA:
        if TEST_WITH_ROCM:
            arch_list = ["gfx942", "gfx950"]
            for arch in arch_list:
                if arch in torch.cuda.get_device_properties(0).gcnArchName:
                    return True
            return False
        else:
            return True
    else:
        return False

