import os

def evaluate_gfx_arch_within(arch_list):
    if not torch.cuda.is_available():
        return False
    gcn_arch_name = torch.cuda.get_device_properties('cuda').gcnArchName
    effective_arch = os.environ.get('PYTORCH_DEBUG_FLASH_ATTENTION_GCN_ARCH_OVERRIDE', gcn_arch_name)
    # gcnArchName can be complicated strings like gfx90a:sramecc+:xnack-
    # Hence the matching should be done reversely
    return any(arch in effective_arch for arch in arch_list)

