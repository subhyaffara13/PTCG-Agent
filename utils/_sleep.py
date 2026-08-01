
def _sleep(cycles):
    torch._C._cuda_sleep(cycles)

