
def get_rtol(dtype):
    # Choose a safe rtol
    if dtype in (single, csingle):
        return 1e-5
    else:
        return 1e-11

