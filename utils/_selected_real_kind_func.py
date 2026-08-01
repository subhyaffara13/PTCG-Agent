
def _selected_real_kind_func(p, r=0, radix=0):
    # XXX: This should be processor dependent
    # This is only verified for 0 <= p <= 20, possibly good for p <= 33 and above
    if p < 7:
        return 4
    if p < 16:
        return 8
    machine = platform.machine().lower()
    if machine.startswith(('aarch64', 'alpha', 'arm64', 'loongarch', 'mips', 'power', 'ppc', 'riscv', 's390x', 'sparc')):
        if p <= 33:
            return 16
    elif p < 19:
        return 10
    elif p <= 33:
        return 16
    return -1

