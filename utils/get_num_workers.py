
def get_num_workers() -> int:
    if "TORCHINDUCTOR_COMPILE_THREADS" in os.environ:
        return int(os.environ["TORCHINDUCTOR_COMPILE_THREADS"])

    cpu_count = torch._utils.cpu_count()
    assert cpu_count

    # Divide the number of CPUs by the number of GPUs for distributed workloads
    if (
        config.is_fbcode()
        and torch.cuda.is_available()
        and torch.cuda.device_count() > 0
    ):
        cpu_count = cpu_count // torch.cuda.device_count()

    return cpu_count

