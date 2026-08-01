
def is_navi3_arch():
    if torch.cuda.is_available():
        prop = torch.cuda.get_device_properties(0)
        gfx_arch = prop.gcnArchName.split(":")[0]
        if gfx_arch in NAVI3_ARCH:
            return True
    return False

