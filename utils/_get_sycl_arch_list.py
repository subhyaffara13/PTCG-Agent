
def _get_sycl_arch_list():
    if 'TORCH_XPU_ARCH_LIST' in os.environ:
        return os.environ.get('TORCH_XPU_ARCH_LIST')
    arch_list = torch.xpu.get_arch_list()
    # Dropping dg2* archs since they lack hardware support for fp64 and require
    # special consideration from the user. If needed these platforms can
    # be requested thru TORCH_XPU_ARCH_LIST environment variable.
    arch_list = [x for x in arch_list if not x.startswith('dg2')]
    return ','.join(arch_list)

