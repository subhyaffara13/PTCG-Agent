
def _macos_arch(machine):
    return {'PowerPC': 'ppc', 'Power_Macintosh': 'ppc'}.get(machine, machine)

