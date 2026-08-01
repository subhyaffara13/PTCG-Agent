
def test_public_modules_importable_2():
    # Ensure we use max 6 processes, to limit peak resource usage (memory, file handles)
    # on resource-constrained systems (e.g., RISC-V - see gh-24163).
    with multiprocessing.Pool(processes=6) as pool:
        pool.map(_check_single_module, PUBLIC_MODULES)

